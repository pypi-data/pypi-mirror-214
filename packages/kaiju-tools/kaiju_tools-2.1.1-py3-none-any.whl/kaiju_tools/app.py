import abc
import asyncio
import errno
import logging
import uuid
from argparse import ArgumentParser
from enum import Enum
from time import time
from typing import Union, List, Type, TypeVar, Optional, Iterable, cast, TypedDict, Awaitable, Callable
from contextvars import ContextVar  # noqa pycharm
from weakref import proxy

from aiohttp.web import Application, run_app, AppRunner

from kaiju_tools.config import ConfigLoader, ProjectSettings
from kaiju_tools.class_registry import AbstractClassRegistry
from kaiju_tools.functions import retry, timeout
from kaiju_tools.types import App, Scope, Session, RequestContext, ServiceConfig, Namespace, SHARED_NS, SortedStack
from kaiju_tools.loop import loop
from kaiju_tools.logging import Adapter, HANDLERS, FORMATTERS, Logger

__all__ = [
    'App',
    'Service',
    'ContextableService',
    'ServiceClassRegistry',
    'service_class_registry',
    'ServiceConfigurationError',
    'ServiceContextManager',
    'Scope',
    'Session',
    'RequestContext',
    'run_command',
    'Commands',
    'AbstractCommand',
    'LoggingService',
    'Scheduler',
    'ExecPolicy',
]


class Service(abc.ABC):
    """Base service class."""

    service_name = None  #: you may define a custom service name here

    def __init__(self, app: App = None, logger=None):
        """Initialize.

        :param app: aiohttp web application
        :param logger: a logger instance (None for default)
        """
        self.app = app
        self.log_ctx = {}
        if logger is None:
            if app:
                logger = logging.getLogger(self.app.name)
            else:
                logger = logging.getLogger('root')
        self.logger = Adapter(logger, self.log_ctx)

    def discover_service(
        self,
        name: Union[str, 'Service', None],
        cls: Union[Union[str, Type], Iterable[Union[str, Type]]] = None,
        required=True,
    ):
        """Discover a service using specified name and/or service class.

        :param name: specify a service name or service instance (in latter case
            it will be returned as is)
            False means that nothing will be returned, i.e. service will be disabled
        :param cls: specify service class. If name wasn't specified, then the first
            service matching given class will be returned. If name and class
            both were specified, then the type check will be performed on a newly
            discovered service
        :param required: means that an exception will rise if service doesn't exist
            otherwise in this case None will be returned
        """
        if name is False and not required:
            return
        elif isinstance(name, Service):
            return name
        else:
            return self.app.services.discover_service(name=name, cls=cls, required=required)  # noqa ?


class ContextableService(Service):
    """A service which must be asynchronously initialized after it was created."""

    async def init(self):
        """Define your asynchronous initialization here."""

    async def close(self):
        """Define your asynchronous de-initialization here."""

    @property
    def closed(self) -> bool:
        """Must return True if `close()` procedure has been successfully executed."""
        return False

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


Contextable = ContextableService


class ServiceConfigurationError(RuntimeError):
    """An error during services configuration or initialization."""


class ServiceNotAvailableError(KeyError):
    """Service with such name doesn't exist."""


class ServiceClassRegistry(AbstractClassRegistry):
    """Class registry for service classes."""

    base_classes = [Service]


service_class_registry = ServiceClassRegistry(raise_if_exists=False)  #: default service class registry object

_Service = TypeVar('_Service', bound=Service)


class ServiceContextManager(ContextableService):
    """Services manager."""

    service_name = 'srv'

    def __init__(
        self,
        app: App,
        settings: List[Union[ServiceConfig, str]],
        class_registry: ServiceClassRegistry = service_class_registry,
        logger=None,
    ):
        """Initialize."""
        super().__init__(app=app, logger=logger)
        self._settings = settings
        self._registry = class_registry
        self._required = set()
        self._running_services = []
        self._services = {}

    async def init(self):
        self._create_services()
        for name, service in self._services.items():
            try:
                await self.start_service(name)
            except Exception as exc:
                if name in self._required:
                    await self.close()
                    raise
                else:
                    self.logger.error('Service failed', service=name, exc_info=exc)

    async def close(self):
        for name in self._running_services[::-1]:
            await self.terminate_service(name)
        self._running_services.clear()

    async def start_service(self, name: str) -> None:
        """Start an idle service."""
        service = self._services[name]
        if name in self._running_services:
            return
        if isinstance(service, ContextableService):
            self.logger.debug('Starting service', service=service.service_name)
            await service.init()
            self._running_services.append(name)

    async def terminate_service(self, name: str) -> None:
        """Terminate a running service."""
        service = self._services[name]
        if name not in self._running_services:
            return
        if isinstance(service, ContextableService):
            self.logger.debug('Closing service', service=service.service_name)
            try:
                await service.close()
            except Exception as exc:
                self.logger.error('Service failed to close', service=name, exc_info=exc)
        self._running_services.remove(name)

    async def cleanup_context(self, _):
        """Get aiohttp cleanup context."""
        await self.init()
        yield
        await self.close()

    def __getattr__(self, item):
        return self._services[item]

    def __getitem__(self, item):
        return self._services[item]

    def __contains__(self, item):
        return item in self._services

    def items(self):
        return self._services.items()

    def discover_service(
        self,
        name: Union[str, _Service] = None,
        cls: Type[_Service] = None,
        required: bool = True,
    ) -> Optional[_Service]:
        """Discover a service using specified name and/or service class.

        :param name: specify a service name or service instance (in latter case
            it will be returned as is)
        :param cls: specify service class or a list of classes. If name wasn't specified,
            then the first service matching given class will be returned. If name and class
            both were specified, then the type check will be performed on a newly
            discovered service. If multiple classes are provided they will be checked in
            priority order one by one.
        :param required: means that an exception will rise if service doesn't exist
            otherwise in this case None will be returned
        """
        if isinstance(name, Service):
            return name

        if name and name in self._services:
            service = self._services[name]
            if not isinstance(service, cls):
                raise ValueError('Service class mismatch.')
            return service

        service = next((service for service in self._services.values() if isinstance(service, cls)), None)
        if service:
            return service
        elif required:
            raise ValueError('Service not found.')

    def _create_services(self) -> None:
        self._services.clear()
        for settings in self._settings:
            if type(settings) is str:
                settings = ServiceConfig(cls=settings)
            if settings.get('enabled', True):
                cls = self._registry[settings['cls']]
                name = settings.get('name', getattr(cls, 'service_name', None))
                if not name:
                    name = cls.__name__
                if name in self._services:
                    if not settings.get('override'):
                        raise ServiceConfigurationError('Service with name "%s" already registered.' % name)
                service = cls(app=self.app, **settings.get('settings', {}), logger=self.logger.getChild(name))
                service.service_name = name
                self._services[name] = service
                if settings.get('required', True):
                    self._required.add(name)
                loglevel = settings.get('loglevel')
                if loglevel:
                    service.logger.setLevel(loglevel)


_Callable = Callable[..., Awaitable]


class ExecPolicy(Enum):
    """Task policy for a scheduled task."""

    WAIT = 'WAIT'  #: wait until the current task iteration is executed
    CANCEL = 'CANCEL'  #: cancel the current iteration immediately and restart the task


class _ScheduledTask:
    """Scheduled task information."""

    __slots__ = (
        '_scheduler',
        'name',
        'method',
        'params',
        'interval',
        'policy',
        'called_at',
        '_enabled',
        'executed',
        'retries',
        '__weakref__',
    )

    def __init__(
        self,
        scheduler: 'Scheduler',
        name: str,
        method: Callable,
        params: Union[dict, None],
        interval: float,
        policy: ExecPolicy,
        retries: int,
    ):
        """Initialize."""
        self._scheduler = proxy(scheduler)
        self.name = name
        self.method = method
        self.params = params
        self.interval = interval
        self.policy = policy
        self.called_at = 0
        self.retries = retries
        self._enabled = True
        self.executed: Union[asyncio.Task, None] = None

    @property
    def enabled(self) -> bool:
        """Task is enabled for execution."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable task."""
        self._enabled = value
        if value is True:
            t_ex = self.called_at + self.interval
            self.scheduler._stack.insert(t_ex, self)  # noqa

    @property
    def max_timeout(self) -> float:
        if self.policy is ExecPolicy.CANCEL:
            return max(0.0, self.interval)
        else:
            return max(0.0, self.interval * 4.0)


class Scheduler(ContextableService):
    """Scheduler for periodic tasks execution."""

    ExecPolicy = ExecPolicy

    def __init__(self, *args, refresh_rate: float = 1.0, **kws):
        """Initialize.

        :param refresh_rate: base refresh rate
        """
        super().__init__(*args, **kws)
        self.refresh_rate = refresh_rate
        self._stack = SortedStack()
        self._tasks: List[_ScheduledTask] = []
        self._scheduler_task: Union[asyncio.Task, None] = None

    async def init(self):
        """Initialize."""
        self._scheduler_task = asyncio.create_task(self._iter())

    async def close(self):
        """Close."""
        self._scheduler_task.cancel()
        self._scheduler_task = None
        self._stack.clear()
        await asyncio.gather(
            *(
                task.executed
                for task in self._tasks
                if task.executed and not (task.executed.done() or task.executed.cancelled())
            ),
            return_exceptions=True,
        )

    @property
    def tasks(self):
        """Get a list of registered tasks."""
        return self._tasks

    def schedule_task(
        self,
        method: _Callable,
        interval: float,
        params: Union[dict, None] = None,
        *,
        policy: ExecPolicy = ExecPolicy.CANCEL,
        retries: int = 0,
        name: str = None,
    ) -> _ScheduledTask:
        """Schedule a periodic task.

        :param method: RPC server method name
        :param params: method input arguments
        :param interval: exec interval in seconds
        :param policy: exec policy
        :param retries: number of retries if any
        :param name: optional custom task name (for tracing)
        :returns: an instance of scheduled task
            you can temporarily suspend this task from execution by settings `task.enabled = False`
            it will not be picked up by the scheduler until you set it back to `True`
        """
        if name is None:
            name = f'scheduled:{method.__name__}'
        if params is None:
            params = {}
        self.logger.debug('schedule', task_name=name, interval=interval, policy=policy.value)
        task = _ScheduledTask(self, name, method, params, interval, policy, retries)
        self._tasks.append(task)
        t_ex = time() + interval
        self._stack.insert(t_ex, task)
        return task

    async def _iter(self) -> None:
        """Iterate over the tasks ready to run."""
        while 1:
            to_execute = self._stack.pop_many(time())
            for scheduled in to_execute:
                scheduled = cast(_ScheduledTask, scheduled)
                if not scheduled.enabled:
                    continue
                if scheduled.executed and not (scheduled.executed.done() or scheduled.executed.cancelled()):
                    if scheduled.policy is ExecPolicy.CANCEL:
                        scheduled.executed.cancel(msg='Cancelled by the scheduler')
                    elif scheduled.policy is ExecPolicy.WAIT:
                        continue

                scheduled.executed = task = asyncio.create_task(self._run_task(scheduled))
                scheduled.called_at = time()
                task._scheduled = proxy(scheduled)
                task.add_done_callback(self._task_callback)
                task.set_name(scheduled.name)

            await asyncio.sleep(self._get_sleep_interval())

    async def _run_task(self, task: _ScheduledTask) -> None:
        """Run task in a wrapper."""
        try:
            async with timeout(task.max_timeout):
                if task.retries:
                    await retry(task.method, kws=task.params, retries=task.retries)
                else:
                    await task.method(**task.params)
        except Exception as exc:
            self.logger.error('task error', task_name=task.name, exc_info=exc)

    def _get_sleep_interval(self) -> float:
        """Get real sleep interval for the scheduler loop."""
        lowest_score = self._stack.lowest_score
        if lowest_score is None:
            lowest_score = 0
        t0 = time()
        interval = min(max(lowest_score - t0, t0), self.refresh_rate)
        return interval

    def _task_callback(self, task: asyncio.Task) -> None:
        """Capture a task result."""
        result = task.result()
        if isinstance(result, Exception):
            self.logger.error(str(result), exc_info=result)
        scheduled = task._scheduled  # noqa
        self._stack.insert(scheduled.called_at + scheduled.interval, scheduled)
        scheduled.executed = None
        task._scheduled = None


class _HandlerSettings(TypedDict, total=False):
    cls: str
    name: str
    formatter: str
    enabled: bool
    settings: dict
    formatter_settings: dict
    loglevel: str


class _LoggerSettings(TypedDict, total=False):
    name: str
    enabled: bool
    handlers: Union[List[str], bool]
    loglevel: str


class LoggingService(ContextableService):
    """Log handler and formatter configuration for application loggers."""

    handler_classes = HANDLERS
    formatter_classes = FORMATTERS

    def __init__(
        self,
        *args,
        loggers: Iterable[_LoggerSettings] = None,
        handlers: Iterable[_HandlerSettings] = None,
        loglevel: str = None,
        **kws,
    ):
        """Initialize."""
        super().__init__(*args, **kws)
        self.loggers = loggers
        self.handlers = handlers
        self.loglevel = loglevel if loglevel else getattr(self.app, 'loglevel', 'INFO')
        self.clear_root_logger()
        _handlers = {handler['name']: handler for handler in self.handlers} if self.handlers else {}
        _loggers = {logger['name']: logger for logger in self.loggers} if self.loggers else {}
        app_logger_name = self.app.logger.name
        if app_logger_name not in _loggers:
            _loggers[app_logger_name] = _LoggerSettings(name=app_logger_name, enabled=True, handlers=True)
        self._handlers = {  # noqa
            name: self._init_handler(handler) for name, handler in _handlers.items() if handler.get('enabled')
        }
        self._loggers = {  # noqa
            name: self._init_logger(logger) for name, logger in _loggers.items() if logger.get('enabled')
        }

    def get_logger(self, logger: Union[Logger, Adapter] = None, log_ctx: dict = None):
        """Get a new logger instance.

        :param logger: base logger (None for app logger)
        :param log_ctx: service log context, may contain various service context metadata
        """
        if logger is None:
            logger = logging.getLogger(self.app.name)
        if log_ctx is None:
            log_ctx = {}
        return Adapter(logger, log_ctx)

    @staticmethod
    def clear_root_logger():
        """Remove all existing handlers from the root logger."""
        logger = logging.getLogger()
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)

    def _init_handler(self, handler: _HandlerSettings) -> logging.Handler:
        """Initialize a handler with handler settings."""
        if isinstance(handler['cls'], str):
            handler['cls'] = self.handler_classes[handler['cls']]
        if isinstance(handler['formatter'], str):
            handler['formatter'] = self.formatter_classes[handler['formatter']]
        _handler = handler['cls'](self.app, **handler.get('settings', {}))
        formatter = handler['formatter'](**handler.get('formatter_settings', {}))
        _handler.setFormatter(formatter)
        loglevel = handler.get('loglevel', self.loglevel)
        _handler.setLevel(loglevel)
        return _handler

    def _init_logger(self, logger: _LoggerSettings) -> logging.Logger:
        """Initialize a logger with logger settings."""
        _logger = logging.getLogger(logger['name'])
        _logger.handlers = []
        if logger['handlers'] is True:
            _handlers = self._handlers.values()
        else:
            _handlers = (self._handlers[name] for name in logger['handlers'])
        for handler in _handlers:
            _logger.addHandler(handler)
        loglevel = logger.get('loglevel', self.loglevel)
        _logger.setLevel(loglevel)
        return _logger


class AbstractCommand(ContextableService, abc.ABC):
    """Base application command, recognized by CLI."""

    service_name = None  #: command name after `python -m my_app [...]`
    run_app = True

    def __init__(self, app: App, logger=None):
        super().__init__(app=app, logger=logger)
        self._runner = AppRunner(app)
        self._closed = True

    @classmethod
    def get_parser(cls) -> ArgumentParser:
        """Get an argument parser for CLI command arguments."""
        return ArgumentParser()

    @abc.abstractmethod
    async def command(self, **kws):
        """Run a specific command."""

    async def init(self):
        """Initialize."""

    async def close(self):
        """Close command context."""

    @property
    def closed(self) -> bool:
        return self._closed

    def run(self):
        result = 1
        try:
            self.logger.info('Setting up a webapp runner.')
            if self.run_app:
                loop.run_until_complete(self._runner.setup())
            self.logger.info('Initialization.')
            loop.run_until_complete(self.init())
            self._closed = False
            params, _ = self.get_parser().parse_known_args()
            self.logger.info('Executing command "%s" with params: "%s"', self.service_name, params)
            result = loop.run_until_complete(self.command(**params.__dict__))
        except Exception as err:
            self.logger.error('Command failed.', exc_info=err)
        finally:
            self.logger.info('Closing.')
            loop.run_until_complete(self.close())
            if self.run_app:
                loop.run_until_complete(self._runner.cleanup())
            loop.close()
            self._closed = True
            return result


class Commands(AbstractClassRegistry):
    """Map of all available commands. User MUST register it in this class."""

    base_classes = (AbstractCommand,)

    @staticmethod
    def class_key(obj) -> str:
        return obj.service_name


commands = Commands()


def run_command(app: App, command: str, commands_registry=commands) -> int:
    if command in commands_registry:
        cmd = commands_registry[command]
        cmd = cmd(app=app, logger=app.logger.getChild('CLI'))
        result = cmd.run()
    else:
        app.logger.error('Unknown command "%s".', command)
        result = errno.ENOENT
    return result


def init_config(base_config_paths=None, base_env_paths=None, default_env_paths=None) -> (str, ProjectSettings):
    """Configure."""
    if base_config_paths is None:
        base_config_paths = ['./settings/config.yml']
    if base_env_paths is None:
        base_env_paths = ['./settings/env.json']
    if default_env_paths is None:
        default_env_paths = ['./settings/env.local.json']
    logging.basicConfig(level='INFO')
    config_loader = ConfigLoader(
        base_config_paths=base_config_paths, base_env_paths=base_env_paths, default_env_paths=default_env_paths
    )
    command, config = config_loader.configure()
    logging.root.handlers = []
    return command, config


def init_app(settings: ProjectSettings, attrs: dict = None, middlewares: list = None) -> App:
    if middlewares is None:
        middlewares = []
    app = Application(middlewares=middlewares, logger=logging.getLogger(settings.main.name), **settings.app)
    app = cast(App, app)
    app.ns = Namespace(env=app.env, name=app.name)
    app.ns_shared = Namespace(env=app.env, name=SHARED_NS)
    app.id = uuid.uuid4()
    app.loglevel = settings.main['loglevel']
    for key, value in settings.main.items():
        app[key] = value
        setattr(app, key, value)
    if attrs:
        for key, value in attrs.items():
            app[key] = value
            setattr(app, key, value)
    app.settings = settings
    app.services = services = ServiceContextManager(
        app=app, settings=settings.services, class_registry=service_class_registry, logger=app.logger
    )
    app.cleanup_ctx.append(services.cleanup_context)
    return app


def main(_init_app, **config_settings):
    command, config = init_config(**config_settings)
    app: App = _init_app(config)
    if config.app.debug:
        print('\n-- RUNNING IN DEBUG MODE --\n')
    if command:
        run_command(app, command)
    else:
        run_app(app, access_log=False, **config.run)  # noqa
