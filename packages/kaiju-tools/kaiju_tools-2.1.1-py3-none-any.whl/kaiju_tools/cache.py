"""Shared cache services and classes."""

import abc
import asyncio
from typing import Union, Collection, FrozenSet, List, Dict, Any

from kaiju_tools.app import ContextableService, Service
from kaiju_tools.encoding import MimeTypes, serializers
from kaiju_tools.functions import RETRY_EXCEPTION_CLASSES
from kaiju_tools.types import NSKey

__all__ = ['BaseCacheService']


class BaseCacheService(ContextableService, abc.ABC):
    """Base class for shared cache."""

    service_name = 'cache'
    CONNECTION_ERROR_CLASSES = RETRY_EXCEPTION_CLASSES
    DEFAULT_TTL = 0
    DEFAULT_SERIALIZER_TYPE = MimeTypes.msgpack
    IGNORE_CONN_ERRORS = False
    NOWAIT = True
    transport_cls = None

    def __init__(
        self,
        app,
        transport: Union[str, Service] = None,
        default_ttl: int = DEFAULT_TTL,
        serializer_type: str = DEFAULT_SERIALIZER_TYPE,
        encoders=serializers,
        logger=None,
    ):
        """Initialize.

        :param app: web app (provided by the service manager)
        :param transport: transport service (may be Redis, DB or similar)
        :param default_ttl:  default key lifetime in seconds (0 for infinite)
        :param serializer_type: you may specify a serializer type from `kaiju-tools.encoding`
        :param encoders: serializers registry with all serializers classes
        :param logger: logger instance (provided by the service manager)
        """
        Service.__init__(self, app=app, logger=logger)
        self._transport_name = transport
        self._default_ttl = max(self.DEFAULT_TTL, int(default_ttl))
        self._serializer = encoders[serializer_type]()
        self._transport = None
        self._queue = None

    async def init(self):
        """Service context init."""
        self._transport = self.discover_service(self._transport_name, cls=self.transport_cls)

    async def exists(self, key: NSKey, ignore_conn_errors=IGNORE_CONN_ERRORS) -> bool:
        """Check if key is present in the cache."""
        result = await self._wrap_exec(self._exists(key), ignore_conn_errors)
        if result is None:
            self.logger.info('key not found', key=key)
        return bool(result)

    async def _exists(self, key: NSKey) -> bool:
        """Check if such key present and has not expired."""

    async def m_exists(self, keys: Collection[NSKey], ignore_conn_errors=IGNORE_CONN_ERRORS) -> FrozenSet[NSKey]:
        """Return a set of existing keys."""
        self.logger.debug('m_exists', num_keys=len(keys))
        results = await self._wrap_exec(self._m_exists(*keys), ignore_conn_errors)
        if results:
            return frozenset(NSKey(key) for key, result in zip(keys, results) if bool(result))
        else:
            return frozenset()

    @abc.abstractmethod
    async def _m_exists(self, *keys: NSKey) -> List[NSKey]:
        """Return a list of 0 and 1 (0 for not existing True for existing)."""

    async def get(self, key: NSKey, use_serializer=True, ignore_conn_errors=IGNORE_CONN_ERRORS):
        """Get value of a key or None if not found.

        :param key: string only
        :param use_serializer: to use serializer for value decoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        self.logger.debug('get', key=key)
        value = await self._wrap_exec(self._get(key), ignore_conn_errors)
        value = self._load_value(value, use_serializer)
        if value is None:
            self.logger.info('key not found', key=key)
        return value

    @abc.abstractmethod
    async def _get(self, key: NSKey):
        """Return a key value or None if not found."""

    async def m_get(
        self, keys: Collection[NSKey], use_serializer=True, ignore_conn_errors=IGNORE_CONN_ERRORS
    ) -> Dict[NSKey, Any]:
        """Get values of multiple keys.

        :param keys: list of keys
        :param use_serializer: use a serializer for value decoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        self.logger.debug('m_get', num_keys=len(keys))
        values = await self._wrap_exec(self._m_get(*keys), ignore_conn_errors)
        if values:
            result = {k: self._load_value(v, use_serializer) for k, v in zip(keys, values) if v}
        else:
            result = {}
        return result

    @abc.abstractmethod
    async def _m_get(self, *keys: NSKey) -> List[NSKey]:
        """Return a list of values for given keys."""

    async def set(
        self,
        key: NSKey,
        value: Any,
        ttl: int = None,
        use_serializer=True,
        ignore_conn_errors=IGNORE_CONN_ERRORS,
        nowait=NOWAIT,
    ) -> None:
        """Set a single key.

        :param key: string only
        :param value: any serializable value
        :param ttl: key lifetime in seconds, 0 for infinite, None for default
        :param use_serializer: use a serializer for value encoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        :param nowait: set operation in background (don't wait for response)
        """
        if ttl is None:
            _ttl = self._default_ttl
        else:
            _ttl = ttl
        self.logger.info('set', key=key, ttl=ttl)
        value = self._dump_value(value, use_serializer)
        _task = self._wrap_exec(self._set(key, value, _ttl), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _set(self, key: NSKey, value: bytes, ttl: int):
        """Set a key value with ttl in sec (0 for infinite)."""

    async def m_set(
        self,
        keys: Dict[NSKey, Any],
        ttl: int = None,
        use_serializer=True,
        ignore_conn_errors=IGNORE_CONN_ERRORS,
        nowait=NOWAIT,
    ):
        """Set multiple keys.

        :param keys: <key>: <value>
        :param ttl: lifetime in seconds, 0 for infinite, None for default
        :param use_serializer: use a serializer for value encoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        :param nowait: set operation in background (don't wait for response)
        """
        if ttl is None:
            _ttl = self._default_ttl
        else:
            _ttl = ttl
        key_dict = {k: self._dump_value(v, use_serializer) for k, v in keys.items()}
        self.logger.info('m_set', keys=list(keys.keys()), ttl=ttl)
        _task = self._wrap_exec(self._m_set(key_dict, _ttl), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _m_set(self, keys: Dict[NSKey, bytes], ttl: int):
        """Set multiple keys at once with ttl in sec (0 for inf)."""

    async def delete(self, key: NSKey, ignore_conn_errors=IGNORE_CONN_ERRORS, nowait=NOWAIT) -> None:
        """Remove a key from cache."""
        self.logger.info('delete', key=key)
        _task = self._wrap_exec(self._delete(key), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _delete(self, key: str):
        """Remove one key at once."""

    async def m_delete(self, keys: Collection[NSKey], ignore_conn_errors=IGNORE_CONN_ERRORS, nowait=NOWAIT) -> None:
        """Remove multiple keys at once."""
        self.logger.info('m_delete', keys=keys)
        _task = self._wrap_exec(self._m_delete(*keys), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _m_delete(self, *keys: NSKey):
        """Remove multiple keys at once."""

    async def _wrap_exec(self, f, ignore_conn_errors: bool):
        try:
            return await f
        except tuple(self.CONNECTION_ERROR_CLASSES):
            if not ignore_conn_errors:
                raise

    def _load_value(self, value, use_serializer: bool):
        if value is None:
            return
        elif use_serializer:
            return self._serializer.loads(value)
        else:
            return value

    def _dump_value(self, value, use_serializer: bool):
        if use_serializer:
            return self._serializer.dumps(value)
        else:
            return value
