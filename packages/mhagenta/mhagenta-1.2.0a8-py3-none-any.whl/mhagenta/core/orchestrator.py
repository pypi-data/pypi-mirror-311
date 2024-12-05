import asyncio
import logging
import os
import shutil
import time
from asyncio import TaskGroup
from dataclasses import dataclass
from io import TextIOWrapper
from os import PathLike
from pathlib import Path
from typing import Any, Iterable, Literal, Self

import dill
import docker
from docker.errors import NotFound
from docker.models.containers import Container
from docker.models.images import Image

import mhagenta
from mhagenta.bases import *
from mhagenta.containers import *
from mhagenta.core.connection import Connector, RabbitMQConnector
from mhagenta.utils.common import DEFAULT_LOG_FORMAT

from mhagenta.gui import Monitor


@dataclass
class AgentEntry:
    agent_id: str
    kwargs: dict[str, Any]
    dir: Path | None = None
    save_dir: Path | None = None
    image: Image | None = None
    container: Container | None = None
    port_mapping: dict[int, int] | None = None
    num_copies: int = 1

    @property
    def module_ids(self) -> list[str]:
        module_ids = []
        keys = ('perceptors',
                'actuators',
                'll_reasoners',
                'learners',
                'knowledge',
                'hl_reasoners',
                'goal_graphs',
                'memory')
        for key in keys:
            if self.kwargs[key] is None:
                continue
            if isinstance(self.kwargs[key], Iterable):
                for module in self.kwargs[key]:
                    module_ids.append(module.module_id)
            else:
                module_ids.append(self.kwargs[key].module_id)
        return module_ids


class Orchestrator:
    """Orchestrator class that handles MHAgentA execution.

    Orchestrator handles definition of agents and their consequent containerization and deployment. It also allows you
    to define default parameters shared by all the agents handles by it (can be overridden by individual agents)

    """
    SAVE_SUBDIR = 'out/save'
    LOG_CHECK_FREQ = 1.
    WRAPPER_IMAGE_TAG = '27.3.1-dind'
    WRAPPER_PYTHON_VERSION = '3.12.7-r0'

    def __init__(self,
                 save_dir: str | PathLike,
                 port_mapping: dict[int, int] | None = None,
                 wrapping: Literal['shared', 'closed', 'none'] = 'none',
                 step_frequency: float = 1.,
                 status_frequency: float = 5.,
                 control_frequency: float = -1.,
                 exec_start_time: float | None = None,
                 agent_start_delay: float = 5.,
                 exec_duration: float = 60.,
                 save_format: Literal['json', 'dill'] = 'json',
                 resume: bool = False,
                 log_level: int = logging.INFO,
                 log_format: str | None = None,
                 status_msg_format: str = '[status_upd]::{}',
                 module_start_delay: float = 2.,
                 connector_cls: type[Connector] = RabbitMQConnector,
                 connector_kwargs: dict[str, Any] | None = None,
                 prerelease: bool = False,
                 wrapper_requirements: list[str] | str | PathLike | None = None,
                 save_logs: bool = True
                 ) -> None:
        """
        Constructor method for Orchestrator.

        Args:
            save_dir (str | PathLike): Root directory for storing agents' states, logs, and temporary files.
            port_mapping (dict[int, int], optional): Mapping between internal docker container ports and host ports.
            wrapping (Literal['shared', 'closed', 'none'], optional): Specify whether to wrap agents container in
                another container, and if so whether to use the host's network for the wrapping container. This option
                unifies the way the host's network is accessed from the agents' containers.
            step_frequency (float, optional, default=1.0): For agent modules with periodic step functions, the
                frequency in seconds of the step function calls that modules will try to maintain (unless their
                execution takes longer, then the next iteration will be scheduled without a time delay).
            status_frequency (float, optional, default=10.0): Frequency with which agent modules will report their
                statuses to the agent's root controller (error statuses will be reported immediately, regardless of
                the value).
            control_frequency (float, optional): Frequency of agent modules' internal clock when there's no tasks
                pending. If undefined or not positive, there will be no scheduling delay.
            exec_start_time (float, optional): Unix timestamp in seconds of when the agent's execution will try to
                start (unless agent's initialization takes longer than that; in this case the agent will start
                execution as soon as it finishes initializing). If not specified, agents will start execution
                immediately after their initialization.
            agent_start_delay (float, optional, default=5.0): Delay in seconds before agents starts execution. Use when
                `exec_start_time` is not defined to stage synchronous agents start at `agent_start_delay` seconds from
                the `run()` or `arun()` call.
            exec_duration (float, optional, default=60.0):  Time limit for agent execution in seconds. All agents will
                timeout after this time.
            save_format (Literal['json', 'dill'], optional, default='json'): Format of agent modules state save files. JSON
                is more restrictive of what fields the states can include, but it is readable by humans.
            resume (bool, optional, default=False): Specifies whether to use save module states when restarting an
                agent with preexisting ID.
            log_level (int, optional, default=logging.INFO): Logging level.
            log_format (str, optional): Format of agent log messages. Defaults to
                `[%(agent_time)f|%(mod_time)f|%(exec_time)s][%(levelname)s]::%(tags)s::%(message)s`
            status_msg_format (str, optional): Format of agent status messages for external monitoring. Defaults to
                `[status_upd]::{}`
            connector_cls (type[Connector], optional, default=RabbitMQConnector): internal connector class that
                implements communication between modules. MHAgentA agents use RabbitMQ-based connectors by default.
            connector_kwargs (dict[str, Any], optional): Additional keyword arguments for connector. For
                RabbitMQConnector, the default parameters are: {`host`: 'localhost', `port`: 5672, `prefetch_count`: 1}.
            prerelease (bool, optional, default=False): Specifies whether to allow agents to use the latest prerelease
                version of mhagenta while building the container.
            wrapper_requirements (list[str] | str | PathLike): if using a global wrapper, specifies the requirements to be
                installed with `pip install` inside the wrapper container. Can be either a list of packages to
                install or a path to a requirements file.
            save_logs (bool, optional, default=True): Whether to save agent logs. If True, saves each agent's logs to
                `<agent_id>.log` at the root of the `save_dir`. Defaults to True.
        """
        self._agents: dict[str, AgentEntry] = dict()

        save_dir = Path(save_dir).absolute()
        if isinstance(save_dir, str):
            save_dir = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)
        self._save_dir = save_dir

        self._package_dir = str(Path(mhagenta.__file__).parent.absolute())

        self._connector_cls = connector_cls if connector_cls else RabbitMQConnector
        if connector_kwargs is None and connector_cls == RabbitMQConnector:
            self._connector_kwargs = {
                'host': 'localhost',
                'port': 5672,
                'prefetch_count': 1
            }
        else:
            self._connector_kwargs = connector_kwargs

        self._port_mapping = port_mapping if port_mapping else {}
        self._wrapping = wrapping
        self._wrapper_requirements = wrapper_requirements

        self._step_frequency = step_frequency
        self._status_frequency = status_frequency
        self._control_frequency = control_frequency
        self._module_start_delay = module_start_delay
        self._exec_start_time = exec_start_time
        self._exec_duration_sec = exec_duration
        self._agent_start_delay = agent_start_delay

        self._save_format = save_format
        self._resume = resume

        self._log_level = log_level
        self._log_format = log_format if log_format else DEFAULT_LOG_FORMAT
        self._status_msg_format = status_msg_format

        self._prerelease = prerelease
        self._save_logs = save_logs

        self._start_time: float = -1.
        self._simulation_end_ts = -1.

        self._docker_client: docker.DockerClient | None = None
        self._rabbitmq_image: Image | None = None
        self._base_image: Image | None = None

        self._task_group: TaskGroup | None = None
        self._force_run = False

        self._docker_init()

        self._monitor: Monitor | None = None

        self._running = False
        self._stopping = False
        self._all_stopped = False

    def _docker_init(self) -> None:
        self._docker_client = docker.from_env()

    def add_agent(self,
                  agent_id: str,
                  perceptors: Iterable[PerceptorBase] | PerceptorBase,
                  actuators: Iterable[ActuatorBase] | ActuatorBase,
                  ll_reasoners: Iterable[LLReasonerBase] | LLReasonerBase,
                  learners: Iterable[LearnerBase] | LearnerBase | None = None,
                  knowledge: Iterable[KnowledgeBase] | KnowledgeBase | None = None,
                  hl_reasoners: Iterable[HLReasonerBase] | HLReasonerBase | None = None,
                  goal_graphs: Iterable[GoalGraphBase] | GoalGraphBase | None = None,
                  memory: Iterable[MemoryBase] | MemoryBase | None = None,
                  num_copies: int = 1,
                  step_frequency: float | None = None,
                  status_frequency: float | None = None,
                  control_frequency: float | None = None,
                  exec_start_time: float | None = None,
                  start_delay: float = 0.,
                  exec_duration: float | None = None,
                  resume: bool | None = None,
                  log_level: int | None = None,
                  port_mapping: dict[int, int] | None = None,
                  connector_cls: type[Connector] | None = None,
                  connector_kwargs: dict[str, Any] | None = None,
                  save_logs: bool | None = None
                  ) -> None:
        """Define an agent model to be added to the execution.

        This can be either a single agent, a set of identical agents following the same structure model.

        Args:
            agent_id (str): A unique identifier for the agent.
            perceptors (Iterable[PerceptorBase] | PerceptorBase): Definition(s) of agent's perceptor(s).
            actuators (Iterable[ActuatorBase] | ActuatorBase): Definition(s) of agent's actuator(s).
            ll_reasoners (Iterable[LLReasonerBase] | LLReasonerBase): Definition(s) of agent's ll_reasoner(s).
            learners (Iterable[LearnerBase] | LearnerBase, optional): Definition(s) of agent's learner(s).
            knowledge (Iterable[KnowledgeBase] | KnowledgeBase, optional): Definition(s) of agent's knowledge model(s).
            hl_reasoners (Iterable[HLReasonerBase] | HLReasonerBase, optional): Definition(s) of agent's hl_reasoner(s).
            goal_graphs (Iterable[GoalGraphBase] | GoalGraphBase, optional): Definition(s) of agent's goal_graph(s).
            memory (Iterable[MemoryBase] | MemoryBase, optional): Definition(s) of agent's memory structure(s).
            num_copies (int, optional, default=1): Number of copies of the agent to instantiate at runtime.
            step_frequency (float, optional): For agent modules with periodic step functions, the frequency in seconds
                of the step function calls that modules will try to maintain (unless their execution takes longer, then
                the next iteration will be scheduled without a time delay). Defaults to the Orchestrator's
                `step_frequency`.
            status_frequency (float, optional): Frequency with which agent modules will report their statuses to the
                agent's root controller (error statuses will be reported immediately, regardless of the value).
                Defaults to the Orchestrator's `status_frequency`.
            control_frequency (float, optional): Frequency of agent modules' internal clock when there's no tasks
                pending. If undefined or not positive, there will be no scheduling delay. Defaults to the
                Orchestrator's `control_frequency`.
            exec_start_time (float, optional): Unix timestamp in seconds of when the agent's execution will try to
                start (unless agent's initialization takes longer than that; in this case the agent will start
                execution as soon as it finishes initializing). Defaults to the Orchestrator's `exec_start_time`.
            start_delay (float, optional, default=0.0): A time offset from the global execution time start when this agent will
                attempt to start its own execution.
            exec_duration (float, optional): Time limit for agent execution in seconds. The agent will timeout after
                this time. Defaults to the Orchestrator's `exec_duration`.
            resume (bool, optional): Specifies whether to use save module states when restarting an agent with
                preexisting ID. Defaults to the Orchestrator's `resume`.
            log_level (int, optional):  Logging level for the agent. Defaults to the Orchestrator's `log_level`.
            port_mapping (dict[int, int], optional): Mapping between internal docker container ports and host ports.
                Defaults to the Orchestrator's `port_mapping`.
            connector_cls (type[Connector], optional): internal connector class that implements communication between
                modules. Defaults to the Orchestrator's `connector_cls`.
            connector_kwargs (dict[str, Any], optional): Additional keyword arguments for connector. Defaults to
                the Orchestrator's `connector_kwargs`.
            save_logs (bool, optional): Whether to save agent logs. If True, saves the agent's logs to
                `<agent_id>.log` at the root of the `save_dir`. Defaults to the orchestrator's `save_logs`.

        """
        kwargs = {
            'agent_id': agent_id,
            'connector_cls': connector_cls if connector_cls else self._connector_cls,
            'perceptors': perceptors,
            'actuators': actuators,
            'll_reasoners': ll_reasoners,
            'learners': learners,
            'knowledge': knowledge,
            'hl_reasoners': hl_reasoners,
            'goal_graphs': goal_graphs,
            'memory': memory,
            'connector_kwargs': connector_kwargs if connector_kwargs else self._connector_kwargs,
            'step_frequency': self._step_frequency if step_frequency is None else step_frequency,
            'status_frequency': self._status_frequency if status_frequency is None else status_frequency,
            'control_frequency': self._control_frequency if control_frequency is None else control_frequency,
            'exec_start_time': self._exec_start_time if exec_start_time is None else exec_start_time,
            'start_delay': start_delay,
            'exec_duration': self._exec_duration_sec if exec_duration is None else exec_duration,
            'save_dir': f'/{self.SAVE_SUBDIR}/{agent_id}',
            'save_format': self._save_format,
            'resume': self._resume if resume is None else resume,
            'log_level': self._log_level if log_level is None else log_level,
            'log_format': self._log_format,
            'status_msg_format': self._status_msg_format
        }

        self._agents[agent_id] = AgentEntry(
            agent_id=agent_id,
            port_mapping=port_mapping if port_mapping else self._port_mapping,
            num_copies=num_copies,
            kwargs=kwargs
        )
        if self._task_group is not None:
            self._task_group.create_task(self._run_agent(self._agents[agent_id], force_run=self._force_run))

    def _docker_build_base(self,
                           rabbitmq_image_name: str = 'mha-rabbitmq',
                           mha_base_image_name: str = 'mha-base',
                           version_tag: str | None = None
                           ) -> None:
        if version_tag is None:
            version_tag = CONTAINER_VERSION
        try:
            print(f'===== PULLING RABBITMQ BASE IMAGE: {REPO}:rmq =====')
            self._docker_client.images.pull('aurontliar/mhagenta', tag='rmq')
            rabbitmq_image_name = REPO
        except docker.errors.ImageNotFound:
            print('Pulling failed...')
            print(f'===== BUILDING RABBITMQ BASE IMAGE: {rabbitmq_image_name}:{version_tag} =====')
            if self._rabbitmq_image is None:
                self._rabbitmq_image, _ = (
                    self._docker_client.images.build(path=RABBIT_IMG_PATH,
                                                     tag=f'{rabbitmq_image_name}:{version_tag}',
                                                     rm=True,
                                                     quiet=False
                                                     ))

        print(f'===== BUILDING AGENT BASE IMAGE: {mha_base_image_name}:{version_tag} =====')
        if self._base_image is None:
            try:
                self._base_image = self._docker_client.images.list(name=f'{mha_base_image_name}:{version_tag}')[0]
            except IndexError:
                build_dir = self._save_dir.absolute() / 'tmp/'
                try:
                    shutil.copytree(BASE_IMG_PATH, build_dir)
                    shutil.copytree(self._package_dir, build_dir / 'mhagenta')

                    self._base_image, _ = (
                        self._docker_client.images.build(path=str(build_dir),
                                                         buildargs={
                                                             'SRC_IMAGE': rabbitmq_image_name,
                                                             'SRC_VERSION': 'rmq',
                                                             'PRE_VERSION': "true" if self._prerelease else "false"
                                                         },
                                                         tag=f'{mha_base_image_name}:{version_tag}',
                                                         rm=True,
                                                         quiet=False
                                                         ))
                except Exception as ex:
                    shutil.rmtree(build_dir, ignore_errors=True)
                    raise ex
                shutil.rmtree(build_dir)

    def _docker_build_agent(self,
                            agent: AgentEntry
                            ) -> None:
        print(f'===== BUILDING AGENT IMAGE: mhagent:{agent.agent_id} =====')
        agent_dir = self._save_dir.absolute() / agent.agent_id
        if self._force_run and agent_dir.exists():
            shutil.rmtree(agent_dir)

        (agent_dir / 'out/').mkdir(parents=True)
        agent.dir = agent_dir
        agent.save_dir = agent_dir / 'out' / 'save' / agent.agent_id

        build_dir = agent_dir / 'tmp/'
        shutil.copytree(AGENT_IMG_PATH, build_dir.absolute())
        (build_dir / 'src').mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(mhagenta.core.__file__).parent.absolute() / 'agent_launcher.py', (build_dir / 'src' / 'agent_launcher.py').absolute())
        shutil.copy(Path(mhagenta.__file__).parent.absolute() / 'scripts' / 'start.sh', (build_dir / 'src' / 'start.sh').absolute())

        if agent.kwargs['exec_start_time'] is None:
            agent.kwargs['exec_start_time'] = self._start_time
        agent.kwargs['exec_start_time'] += self._agent_start_delay

        end_estimate = agent.kwargs['exec_start_time'] + agent.kwargs['start_delay'] + agent.kwargs['exec_duration']
        if self._simulation_end_ts < end_estimate:
            self._simulation_end_ts = end_estimate

        with open((build_dir / 'src' / 'agent_params').absolute(), 'wb') as f:
            dill.dump(agent.kwargs, f, recurse=True)

        base_tag = self._base_image.tags[0].split(':')
        agent.image, _ = self._docker_client.images.build(path=str(build_dir.absolute()),
                                                          buildargs={
                                                              'SRC_IMAGE': base_tag[0],
                                                              'SRC_VERSION': base_tag[1]
                                                          },
                                                          tag=f'mhagent:{agent.agent_id}',
                                                          rm=True,
                                                          quiet=False
                                                          )
        shutil.rmtree(build_dir)

    async def _run_agent(self,
                         agent: AgentEntry,
                         force_run: bool = False
                         ) -> None:
        if agent.num_copies == 1:
            print(f'===== RUNNING AGENT IMAGE \"mhagent:{agent.agent_id}\" AS CONTAINER \"{agent.agent_id}\" =====')
        else:
            print(f'===== RUNNING AGENT IMAGE \"mhagent:{agent.agent_id}\" AS '
                  f'{agent.num_copies} CONTAINERS \"{agent.agent_id}_#\" =====')
        for i in range(agent.num_copies):
            if agent.num_copies == 1:
                agent_name = agent.agent_id
                agent_dir = (agent.dir / "out").absolute()
            else:
                agent_name = f'{agent.agent_id}_{i}'
                agent_dir = (agent.dir / str(i) / "out").absolute()

            agent_dir.mkdir(parents=True, exist_ok=True)
            try:
                container = self._docker_client.containers.get(agent_name)
                if force_run:
                    container.remove(force=True)
                else:
                    raise NameError(f'Container {agent_name} already exists')
            except NotFound:
                pass

            agent.container = self._docker_client.containers.run(image=agent.image,
                                                                 detach=True,
                                                                 name=agent_name,
                                                                 environment={"AGENT_ID": agent_name},
                                                                 volumes={
                                                                     str(agent_dir): {'bind': '/out', 'mode': 'rw'}
                                                                 },
                                                                 extra_hosts={'host.docker.internal': 'host-gateway'},
                                                                 ports=agent.port_mapping,
                                                                 # links={f'mha-wrapper:{agent_name}'} if self._wrapping == 'handled' else None,
                                                                 tty=True)

    async def arun(self,
                   rabbitmq_image_name: str = 'mha-rabbitmq',
                   mhagent_base_image_name: str = 'mha-base',
                   force_run: bool = False,
                   gui: bool = False
                   ) -> None:
        """Run all the agents as an async method. Use in case you want to control the async task loop yourself.

        Args:
            rabbitmq_image_name (str, optional, default='mha-rabbitmq'): The name of the base MHAgentA RabbitMQ image.
            mhagent_base_image_name (str, optional, default='mha-base'): The name of the base MHAgentA agent image.:
            force_run (bool, optional, default=False): In case containers with some of the specified agent IDs exist,
                specify whether to force remove the old container to run the new ones. Otherwise, an exception will be
                raised.
            gui (bool, optional, default=False): Specifies whether to open the log monitoring window for the
                orchestrator.

        Raises:
            NameError: Raised if a container for one of the specified agent IDs already exists and `force_run` is False.

        """

        if self._base_image is None:
            self._docker_build_base(rabbitmq_image_name=rabbitmq_image_name,
                                    mha_base_image_name=mhagent_base_image_name)

        self._force_run = force_run
        for agent in self._agents.values():
            self._docker_build_agent(agent)

        if gui:
            self._monitor = Monitor()

        self._running = True
        self._start_time = time.time()
        async with asyncio.TaskGroup() as tg:
            self._task_group = tg
            if gui:
                tg.create_task(self._monitor.run())
            for agent in self._agents.values():
                tg.create_task(self._run_agent(agent, force_run=force_run))
                tg.create_task(self._simulation_end_timer())
                tg.create_task(self._read_logs(agent, gui))
        self._running = False
        for agent in self._agents.values():
            agent.container.remove()
        print('===== EXECUTION FINISHED =====')

    def run(self,
            rabbitmq_image_name: str = 'mha-rabbitmq',
            mhagent_base_image_name: str = 'mha-base',
            force_run: bool = False,
            gui: bool = False
            ) -> None:
        """Run all the agents.

        Args:
            rabbitmq_image_name (str, optional, default='mha-rabbitmq'): The name of the base MHAgentA RabbitMQ image.
            mhagent_base_image_name (str, optional, default='mha-base'): The name of the base MHAgentA agent image.:
            force_run (bool, optional, default=False): In case containers with some of the specified agent IDs exist,
                specify whether to force remove the old container to run the new ones. Otherwise, an exception will be
                raised.
            gui (bool, optional, default=False): Specifies whether to open the log monitoring window for the
                orchestrator.

        Raises:
            NameError: Raised if a container for one of the specified agent IDs already exists and `force_run` is False.

        """
        if self._wrapping == 'closed' or self._wrapping == 'shared':
            run_wrapper(
                orchestrator=self,
                rabbitmq_image_name=rabbitmq_image_name,
                mhagent_base_image_name=mhagent_base_image_name,
                force_run=force_run,
                gui=gui
            )
            return

        asyncio.run(self.arun(
            rabbitmq_image_name=rabbitmq_image_name,
            mhagent_base_image_name=mhagent_base_image_name,
            force_run=force_run,
            gui=gui
        ))

    @staticmethod
    def _agent_stopped(agent: AgentEntry) -> bool:
        agent.container.reload()
        return agent.container.status == 'exited'

    @property
    def _agents_stopped(self) -> bool:
        if self._all_stopped:
            return True
        for agent in self._agents.values():
            if not self._agent_stopped(agent):
                return False
        self._all_stopped = True
        return True

    async def _simulation_end_timer(self) -> None:
        await asyncio.sleep(self._simulation_end_ts - time.time())
        self._stopping = True

    def _add_log(self, log: str | bytes, gui: bool = False, file_stream: TextIOWrapper | None = None) -> None:
        if isinstance(log, bytes):
            log = log.decode().strip('\n\r')
        print(log)
        if gui:
            self._monitor.add_log(log)
        if file_stream is not None:
            file_stream.write(f'{log}\n')
            file_stream.flush()

    async def _read_logs(self, agent: AgentEntry, gui: bool = False) -> None:
        logs = self._docker_client.containers.get(agent.container.id).logs(stdout=True, stderr=True, stream=True, follow=True)
        if gui:
            module_ids = agent.module_ids
            module_ids.insert(0, 'root')
            self._monitor.add_agent(agent.agent_id, module_ids)

        if self._save_logs:
            f = open(self._save_dir / f'{agent.agent_id}.log', 'w')
        else:
            f = None
        while True:
            if self._stopping and self._agents_stopped:
                if f is not None:
                    f.close()
                break
            for line in logs:
                self._add_log(line, gui=gui, file_stream=f)
                await asyncio.sleep(0)
            await asyncio.sleep(self.LOG_CHECK_FREQ)

    def __getitem__(self, agent_id: str) -> AgentEntry:
        return self._agents[agent_id]


def run_wrapper(orchestrator: Orchestrator,
                rabbitmq_image_name: str = 'mha-rabbitmq',
                mhagent_base_image_name: str = 'mha-base',
                force_run: bool = False,
                gui: bool = False
                ) -> None:
    file = orchestrator._save_dir / f'_orchestrator'
    host_save_dir = orchestrator._save_dir
    orchestrator._save_dir = '/mha-save'
    client = orchestrator._docker_client
    orchestrator._docker_client = None
    wrap_mode = orchestrator._wrapping
    orchestrator._wrapping = 'handled'
    with open(file.absolute(), 'wb') as f:
        dill.dump(orchestrator, f, recurse=True)
    with open(host_save_dir / '_params', 'wb') as f:
        dill.dump({
            'rabbitmq_image_name': rabbitmq_image_name,
            'mhagent_base_image_name': mhagent_base_image_name,
            'force_run': force_run,
            'gui': gui
        }, f, recurse=True)
    os.makedirs(host_save_dir / '_req', exist_ok=True)
    if isinstance(orchestrator._wrapper_requirements, list):
        with open(host_save_dir / '_req/requirements.txt', 'w') as f:
            f.write('/n'.join(orchestrator._wrapper_requirements))
    elif orchestrator._wrapper_requirements is not None:
        shutil.copy(orchestrator._wrapper_requirements, host_save_dir / '_req/requirements.txt')
    else:
        with open(host_save_dir / '_req/requirements.txt', 'w') as f:
            f.write('')
    os.makedirs(host_save_dir / 'src', exist_ok=True)
    shutil.copy(Path(mhagenta.core.__file__).parent.absolute() / 'orchestrator_launcher.py', (host_save_dir / 'src' / 'orchestrator_launcher.py').absolute())
    shutil.copy(Path(mhagenta.__file__).parent.absolute() / 'scripts' / 'run_orchestrator.sh', (host_save_dir / 'src' / 'run_orchestrator.sh').absolute())

    wrapper = client.images.pull('docker', tag=orchestrator.WRAPPER_IMAGE_TAG)
    container = client.containers.run(image=wrapper,
                                      name='mha-wrapper',
                                      environment={'PRE_VERSION': 'true' if orchestrator._prerelease else 'false'},
                                      volumes={
                                          str(host_save_dir): {'bind': str(orchestrator._save_dir), 'mode': 'rw'}
                                      },
                                      network_mode='host' if wrap_mode == 'shared' else 'bridge',
                                      privileged=True,
                                      remove=True,
                                      detach=True,
                                      stdout=False,
                                      stderr=False,
                                      tty=True
                                      )
    time.sleep(5)
    _, exec_log = container.exec_run(
        ['/bin/sh', f'{orchestrator._save_dir}/src/run_orchestrator.sh'],
        stdout=True,
        stderr=True,
        stream=True,
        tty=True
    )
    orchestrator._save_dir = host_save_dir
    orchestrator._wrapping = wrap_mode
    orchestrator._docker_client = client

    for log in exec_log:
        log = log.decode().split('\n')
        for line in log:
            if line.strip():
                print(line)

    container.stop()
