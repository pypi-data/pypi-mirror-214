"""Shared locks management."""

import abc
import asyncio
from time import time
from typing import Optional, Union, List, NewType, FrozenSet, Dict

from kaiju_tools.app import ContextableService, Service, Scheduler
from kaiju_tools.types import NSKey

__all__ = [
    'BaseLocksService',
    'ErrorCode',
    'LockError',
    'LockExistsError',
    'NotLockOwnerError',
    'LockTimeout',
    'LockId',
]

LockId = NewType('LockId', str)


class LockError(Exception):
    """Base class for lock related errors."""


class LockExistsError(LockError):
    """The same lock already exists."""


class NotLockOwnerError(LockError):
    """A lock can be released only by its owner."""


class LockTimeout(LockError, TimeoutError):
    """Timeout when trying to acquire a lock."""


class ErrorCode:
    """Status and error codes for locks."""

    LOCK_EXISTS = 'LOCK_EXISTS'  #: the lock already present in the db
    NOT_LOCK_OWNER = 'NOT_OWNER'  #: service trying to release a lock is not a lock owner
    RUNTIME_ERROR = 'RUNTIME_ERROR'  #: any other error
    LOCK_ACQUIRE_TIMEOUT = 'LOCK_ACQUIRE_TIMEOUT'
    OK = 'OK'  #: OK


class BaseLocksService(ContextableService, abc.ABC):
    """Base class for managing shared locks."""

    service_name = 'locks'
    WAIT_RELEASE_REFRESH_INTERVAL = 1  #: (s) interval between tries to acquire a used lock
    MIN_REFRESH_INTERVAL = 1  #: (s) minimal allowed refresh interval for the daemon
    REFRESH_INTERVAL = 60  #: (s) how often locks will be renewed by the daemon
    BASE_TTL = 3 * REFRESH_INTERVAL  #: (s) lifetime of a lock after each renewal
    DELIMITER = '-'
    transport_cls = None

    def __init__(
        self,
        app,
        transport: Service = None,
        refresh_interval: int = REFRESH_INTERVAL,
        scheduler: str = None,
        logger=None,
    ):
        """Initialize.

        :param app: web app (provided by the service manager)
        :param transport: db / redis connector
        :param refresh_interval:  how often locks will be renewed
        :param logger: logger instance (provided by the service manager)
        """
        super().__init__(app=app, logger=logger)
        self._transport_name = transport
        self._refresh_interval = max(self.MIN_REFRESH_INTERVAL, int(refresh_interval))
        self._scheduler: Union[Scheduler, None] = scheduler
        self._keys: Dict[NSKey, int] = {}
        self._closing = False
        self._transport = None
        self._task = None

    async def init(self):
        """Initialize."""
        self._transport = self.discover_service(self._transport_name, cls=self.transport_cls)
        self._scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        self._closing = False
        self._task = self._scheduler.schedule_task(
            self._renew_keys,
            self._refresh_interval,
            name=f'{self.service_name}._renew_keys',
            policy=self._scheduler.ExecPolicy.WAIT,
        )
        self._keys = {}

    async def close(self):
        """Close."""
        self._closing = True
        self._task.enabled = False

    async def wait(self, key: NSKey, timeout: float = None) -> None:
        """Wait for a lock and return when it's released.

        :param key: lock key name
        :param timeout: optional max wait time in seconds

        :raises LockAcquireTimeout: when timeout reached
        :raises LockError: any internal error
        """
        t = 0
        while 1:
            if key in self._keys or key in (await self.m_exists([key])):
                self.logger.debug('wait', key=key)
                await asyncio.sleep(self.WAIT_RELEASE_REFRESH_INTERVAL)
                t += self.WAIT_RELEASE_REFRESH_INTERVAL
                if timeout and t > timeout:
                    raise LockTimeout(ErrorCode.LOCK_ACQUIRE_TIMEOUT)
            else:
                break

    async def acquire(
        self, key: NSKey, identifier: LockId = None, ttl: int = None, wait=True, timeout: float = None
    ) -> LockId:
        """Wait for lock and acquire it.

        :param key: lock name
        :param identifier: service/owner identifier, if id is None then the app['id'] will be used
        :param ttl: optional ttl in seconds, None for eternal (until app exists)
        :param wait: wait for a lock to release (if False then it will raise a `LockError`
            if lock with such key already exists
        :param timeout: optional max wait time in seconds

        :raises LockExistsError:
        :raises LockAcquireTimeout: when timeout's reached
        :raises LockError: any internal error
        """

        def _wait():
            if wait:
                return asyncio.sleep(self.WAIT_RELEASE_REFRESH_INTERVAL)
            raise LockExistsError(ErrorCode.LOCK_EXISTS)

        if identifier is None:
            identifier = LockId(str(self.app['id']))

        t0 = 0

        while 1:
            if ttl is None:
                new_ttl = self.BASE_TTL
            else:
                new_ttl = min(self.BASE_TTL, int(ttl))

            t = int(time()) + 1

            if timeout and t0 > timeout:
                raise LockTimeout(ErrorCode.LOCK_ACQUIRE_TIMEOUT)

            t0 += self.WAIT_RELEASE_REFRESH_INTERVAL

            if self._closing:
                await _wait()
                continue

            if key in self._keys:
                _deadline = self._keys[key]
                if _deadline is None or _deadline > t:
                    await _wait()
                    continue
                else:
                    del self._keys[key]

            try:
                await self._acquire([key], identifier, new_ttl)
            except LockExistsError:
                await _wait()
            except Exception as exc:
                raise LockError(ErrorCode.RUNTIME_ERROR) from exc
            else:
                self.logger.info('locked', key=key)
                self._keys[key] = t + new_ttl if ttl else None
                return identifier

    async def release(self, key: NSKey, identifier: LockId) -> None:
        """Release a lock.

        :param key: lock name
        :param identifier: service/owner identifier
        :raises LockError: if the lock can't be released by this service
        """
        self.logger.debug('release', key=key)
        try:
            await self._release([key], identifier)
        except NotLockOwnerError as exc:
            raise exc
        except Exception as exc:
            raise LockError(ErrorCode.RUNTIME_ERROR) from exc
        self.logger.info('released', key=key)
        if key in self._keys:
            del self._keys[key]

    async def owner(self, key: NSKey) -> Optional[LockId]:
        """Return a current lock owner identifier or None if not found / has no owner."""
        owner = await self._owner(key)
        return LockId(owner)

    async def is_owner(self, key: NSKey) -> bool:
        """Return `True` if the current instance is an owner of this lock."""
        owner = await self._owner(key)
        return str(owner) == str(self.app['id'])

    @abc.abstractmethod
    async def m_exists(self, keys: List[NSKey]) -> FrozenSet[NSKey]:
        """Check if locks with such keys exist. Return a set of existing keys."""

    @abc.abstractmethod
    async def _acquire(self, keys: List[NSKey], identifier: LockId, ttl: int):
        """Set a list of specified keys. Also keep in mind that the operation must be atomic or transactional.

        :param keys: a list of keys
        :param identifier: key value
        :param ttl: key ttl in sec
        :raises `LockExistsError` if lock exists
        """

    @abc.abstractmethod
    async def _release(self, keys: List[NSKey], identifier: LockId) -> None:
        """Release a lock.

        Must raise `NotALockOwnerError` if identifier doesn't match the stored one.
        Also keep in mind that the operation must be atomic or transactional.
        """

    @abc.abstractmethod
    async def _renew(self, keys: List[NSKey], values: List[int]) -> None:
        """Renew keys TTLs with the new provided values (in sec)."""

    @abc.abstractmethod
    async def _owner(self, key: NSKey) -> LockId:
        """Return a key owner or None if there's no key or owner."""

    async def _renew_keys(self):
        """Renew existing locks."""
        t = int(time()) + 1
        keys, values, to_remove = [], [], []

        for key, deadline in self._keys.items():
            if deadline is None:
                keys.append(key)
                values.append(self.BASE_TTL)
            elif deadline <= t:
                to_remove.append(key)
            else:
                keys.append(key)
                ttl = min(deadline - t, self.BASE_TTL)
                values.append(ttl)

        for key in to_remove:
            del self._keys[key]

        if keys:
            await self._renew(keys, values)
