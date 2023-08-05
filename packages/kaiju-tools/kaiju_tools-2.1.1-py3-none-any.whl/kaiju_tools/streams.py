"""Message stream services and classes."""

import abc
import asyncio
from typing import Union, List, TypedDict, cast, Dict, Callable, Awaitable

import kaiju_tools.jsonschema as js
from kaiju_tools.app import ContextableService, Scheduler
from kaiju_tools.locks import BaseLocksService, LockId
from kaiju_tools.rpc import RPCRequest, JSONRPCServer, BaseRPCClientService
from kaiju_tools.types import NSKey, Namespace
from kaiju_tools.logging import Adapter

__all__ = ['Listener', 'Consumer', 'TopicSettings', 'StreamRPCClient', 'Topic']


topic_settings_schema = js.Object(
    {
        'key': js.String(minLength=1),
        'app': js.String(minLength=1, default=None),
        'enabled': js.Boolean(default=True),
        'settings': js.Object(default={}),
    },
    required=['key'],
    additionalProperties=False,
)

topics_settings_schema = js.Array(items=topic_settings_schema)
_topics_settings_schema = js.compile_schema(topics_settings_schema)


class Topic:
    """Default topic names."""

    RPC = 'rpc'
    MANAGER = 'manager'
    EXECUTOR = 'executor'


class TopicSettings(TypedDict):
    """Consumer configuration params."""

    key: str  #: consumer key (topic name without the app / env prefix)
    enabled: bool  #: enable / disable consumer, disabled consumer won't be initialized
    settings: dict  #: `Consumer` class settings (unpacked as kws)


class Consumer(abc.ABC):
    """Stream consumer assigned to a particular topic.

    Consumers are created by a listener from topic settings.
    """

    def __init__(self, key: str, topic_key: NSKey, lock_key: NSKey, rpc: JSONRPCServer, logger: Adapter, **_):
        """Initialize."""
        self.key = key
        self.lock_key = lock_key
        self.topic_key = topic_key
        self.rpc = rpc
        self.logger = logger
        self._unlocked = asyncio.Event()
        self._idle = asyncio.Event()
        self._task = None
        self._handler = None
        self.unlock()

    async def init(self):
        self._task = asyncio.create_task(self._read(), name=f'streams.{self.key}._read')

    async def close(self):
        self._task.cancel(msg='closing')

    async def lock(self) -> None:
        self.logger.info('lock')
        self._unlocked.clear()
        await self._idle.wait()

    def unlock(self) -> None:
        self.logger.info('unlock')
        self._unlocked.set()

    def locked(self) -> bool:
        return not self._unlocked.is_set()

    def add_handler(self, f: Callable[..., Awaitable]) -> None:
        self._handler = f

    @abc.abstractmethod
    async def _read_batch(self) -> list:
        """Get messages from a stream."""

    @abc.abstractmethod
    async def _process_batch(self, batch: list) -> None:
        """Define your own message processing and commit here."""

    async def _process_request(self, body, headers: dict) -> None:
        """Process a single request in a batch."""
        if type(body) is RPCRequest:
            await self.rpc.call(body=body, headers=headers, nowait=True)
        elif self._handler:
            try:
                await self._handler(body)
            except Exception as exc:
                self.logger.error('Handler error', exc_info=exc, topic=self.topic_key, body=body)

    async def _read(self) -> None:
        """Read from a stream."""
        self.logger.info('Starting', topic=self.topic_key)
        while 1:
            await self._unlocked.wait()
            self._idle.clear()
            try:
                batch = await self._read_batch()
                await self._process_batch(batch)
            except Exception as exc:
                self.logger.error('Error in consumer loop', exc_info=exc, topic=self.topic_key)
            finally:
                self._idle.set()


class Listener(ContextableService, abc.ABC):
    """Stream listener capable of publishing and consuming messages."""

    service_name = 'streams'
    consumer_cls = Consumer
    CHECK_LOCKS_INTERVAL = 1  #: (s) interval to check shared locks for existing consumers

    def __init__(
        self,
        *args,
        rpc_service: str = None,
        scheduler: str = None,
        locks_service: str = None,
        topics: List[dict] = None,
        **kws,
    ):
        """Initialize.

        :param rpc_service: rpc server name
        :params scheduler: scheduler name
        :param locks_service: locks service name
        :param topics: topics to listen
        """
        super().__init__(*args, **kws)
        self.topics = cast(List[TopicSettings], _topics_settings_schema(topics))
        self._ns = self.app.ns / self.service_name
        self._ns_stream = self._ns / '_stream'
        self._ns_lock = self._ns / '_lock'
        self.consumers: Dict[str, Consumer] = {}
        self._rpc = rpc_service
        self._scheduler = scheduler
        self._locks: BaseLocksService = locks_service  # noqa
        self._lock_task = None

    async def init(self):
        await super().init()
        self._rpc: JSONRPCServer = self.discover_service(self._rpc, cls=JSONRPCServer)
        self._scheduler: Scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        self._locks: BaseLocksService = self.discover_service(self._locks, cls=BaseLocksService)
        self.consumers = {topic['key']: self._create_consumer(topic) for topic in self.topics if topic['enabled']}
        self._lock_task = self._scheduler.schedule_task(
            self._check_locks,
            self.CHECK_LOCKS_INTERVAL,
            policy=self._scheduler.ExecPolicy.WAIT,
            name=f'{self.service_name}._check_locks',
        )
        await asyncio.gather(*(consumer.init() for consumer in self.consumers))

    async def close(self):
        await super().close()
        await asyncio.wait(
            *(consumer.close() for consumer in self.consumers.values()), return_when=asyncio.ALL_COMPLETED
        )
        self._lock_task.enabled = False

    @abc.abstractmethod
    async def write(self, topic: str, body, *, headers: dict = None, key=None) -> None:
        """Submit a message to a stream.

        :param topic: topic name
        :param body: message body
        :param headers: message headers
        :param key: (optional) unique message id
        """

    async def lock_topic(self, key: str) -> LockId:
        """Lock a topic for all instances."""
        consumer = self.consumers[key]
        self.logger.info('lock_topic', topic=consumer.topic_key)
        await consumer.lock()
        return await self._locks.acquire(consumer.lock_key)

    async def unlock_topic(self, key: str, identifier: LockId) -> None:
        consumer = self.consumers[key]
        self.logger.info('unlock_topic', topic=consumer.topic_key)
        await self._locks.release(consumer.lock_key, identifier)
        consumer.unlock()

    def _create_consumer(self, topic: TopicSettings) -> Consumer:
        """Create consumer for a particular topic."""
        return self.consumer_cls(
            key=topic['key'],
            topic_key=self._ns_stream.get_key(topic['key']),
            lock_key=self._ns_lock.get_key(topic['key']),
            rpc=self._rpc,  # noqa
            logger=self.logger.getChild(topic['key']),
            **topic['settings'],
        )

    async def _check_locks(self) -> None:
        """Check for existing topic locks and lock topics if needed."""
        locks = [c.lock_key for c in self.consumers.values()]
        existing = await self._locks.m_exists(locks)
        to_lock = []
        for c in self.consumers.values():
            if c.lock_key in existing:
                if not c.locked():
                    to_lock.append(c.lock())
            else:
                if c.locked():
                    c.unlock()
        if to_lock:
            await asyncio.gather(*to_lock)


class StreamRPCClient(BaseRPCClientService):
    """Stream client for RPC requests."""

    def __init__(self, *args, app: str, listener_service: str, topic: str = Topic.RPC, **kws):
        """Initialize.

        :param app: application (topic) name
        :param listener_service: stream listener service instance
        :param topic: topic name
        """
        super().__init__(*args, **kws)
        self._topic = Namespace(env=self.app.env, name=app).get_key(topic)
        self._listener: Listener = listener_service  # noqa

    async def init(self):
        self._listener = self.discover_service(self._listener, cls=Listener)
        await super().init()

    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict) -> None:
        """Send an RPC request via stream."""
        if type(body) is list:  # automatically make them notify because stream is a one-way interaction
            for row in body:
                row.id = None
        else:
            body.id = None
        await self._listener.write(self._topic, body, headers=headers)
