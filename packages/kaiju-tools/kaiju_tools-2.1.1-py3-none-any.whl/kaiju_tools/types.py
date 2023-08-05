"""Basic types and constants."""

import logging
import sys
from bisect import bisect, bisect_left, bisect_right
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from time import time
from typing import (
    Optional,
    TypedDict,
    FrozenSet,
    Mapping,
    Iterator,
    Sized,
    Iterable,
    Dict,
    cast,
    NewType,
    MutableMapping,
)
from uuid import UUID
from contextvars import ContextVar  # noqa pycharm

from aiohttp.web import Application

from kaiju_tools.serialization import Serializable
from kaiju_tools.functions import not_implemented


SHARED_NS = '_shared'


class Scope(Enum):
    """Permission scope for application methods."""

    SYSTEM = 0
    ADMIN = 10
    USER = 100
    GUEST = 1000


SCOPE_MAP = {Scope.SYSTEM: 'system', Scope.ADMIN: 'admin', Scope.USER: 'user'}  # used by permission services


class Session(Serializable):
    """User session data."""

    __slots__ = ('id', 'h_agent', 'user_id', 'expires', 'permissions', 'data', 'created', '_stored', '_changed')

    def __init__(
        self,
        *,
        id: str,  # noqa
        h_agent: bytes,
        user_id: Optional[UUID],
        expires: int,
        permissions: FrozenSet[str],
        data: dict,
        created: datetime,
        _stored: bool,
        _changed: bool,
        _loaded: bool,
    ):
        """Initialize.

        :param id:
        :param h_agent:
        :param user_id:
        :param expires:
        :param permissions:
        :param data:
        :param created:
        :param _stored:
        :param _changed:
        :param _loaded:
        """
        self.id = id
        self.h_agent = h_agent
        self.user_id = user_id
        self.expires = expires
        self.permissions = frozenset(permissions)
        self.data = data
        self.created = created
        self._stored = _stored
        self._changed = _changed
        self._loaded = _loaded

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, key, value):
        self.update({key: value})

    @property
    def scope(self) -> Scope:
        """Base user scope."""
        if SCOPE_MAP[Scope.SYSTEM] in self.permissions:
            return Scope.SYSTEM
        elif SCOPE_MAP[Scope.USER] in self.permissions:
            return Scope.USER
        else:
            return Scope.GUEST

    @property
    def stored(self) -> bool:
        """Session should be stored."""
        return self._stored

    @property
    def changed(self) -> bool:
        """Session has changed."""
        return self._changed

    @property
    def loaded(self) -> bool:
        """Session has been loaded from db."""
        return self._loaded

    def update(self, data: dict):
        """Update session data."""
        self.data.update(data)
        self._changed = True

    def clear(self):
        """Clear all session data."""
        self.data.clear()
        self._changed = True

    def repr(self) -> dict:
        """Get object representation."""
        return {slot: getattr(self, slot) for slot in self.__slots__ if not slot.startswith('_')}


class RequestContext(TypedDict):
    """Request context stored for the request chain."""

    correlation_id: str
    session_id: Optional[str]
    request_deadline: Optional[int]


class ServiceConfig(TypedDict, total=False):
    """Service configuration parameters."""

    cls: str  #: service class name as in :py:class:`~kaiju_tools.services.service_class_registry`
    name: str  #: unique service name, each service should have a default value for this
    enabled: bool  #: disable service
    required: bool  #: skip a service and proceed on initialization error
    override: bool  #: replace an existing service with the same name
    settings: dict  #: custom settings, unpacked to a service's __init__


class App(Application):
    """Web application interface."""

    id: str
    name: str
    version: str
    env: str
    debug: bool
    loglevel: str
    logger: logging.Logger
    services: dict
    settings: dict
    ns: 'Namespace'
    ns_shared: 'Namespace'

    def get_context(self) -> RequestContext:
        ...

    def get_session(self) -> Optional[Session]:
        ...


class SortedStack(Sized, Iterable):
    """A sorted collection (stack) of items.

    >>> stack = SortedStack({'dogs': 12, 'sobaki': 5})
    >>> stack = SortedStack(stack)
    >>> stack.extend(SortedStack({'cats': 5}))

    Selection:

    >>> stack.select(8)
    ['sobaki', 'cats']

    >>> stack.rselect(8)
    ['dogs']

    Insertion and removal:

    >>> stack.insert(1, 'koty')
    >>> stack.pop_many(3)
    ['koty']

    >>> stack.pop()
    'sobaki'

    >>> len(stack)
    2

    >>> stack.clear()
    >>> bool(stack)
    False

    """

    __slots__ = ('_scores', '_values')

    def __init__(self, __items: Iterable = None):
        self._scores = []
        self._values = []
        if __items:
            self.extend(__items)

    def __iter__(self):
        return iter(zip(self._values, self._scores))

    def __len__(self):
        return len(self._values)

    def __delitem__(self, __item):
        del self._scores[__item]
        del self._values[__item]

    @property
    def lowest_score(self):
        """Get the lowest score in the stack."""
        return next(iter(self._scores), None)

    def extend(self, items: Iterable, /):
        """Extend the stack by adding more than one element."""
        if isinstance(items, dict):
            items = items.items()
        for item, score in items:
            self.insert(score, item)

    def insert(self, score, item, /):
        """Insert a single element into the stack."""
        idx = bisect(self._scores, score)
        self._scores.insert(idx, score)
        self._values.insert(idx, item)

    def select(self, score_threshold, /) -> list:
        """Select and return items without removing them from the lowest score to `score_threshold`.

        The values are guaranteed to be in order.
        """
        return self._select(score_threshold, reverse=False)

    def rselect(self, score_threshold, /) -> list:
        """Select and return items without removing them from the highest score to `score_threshold`.

        The values are guaranteed to be in order.
        """
        return self._select(score_threshold, reverse=True)

    def pop(self):
        """Pop a single element which has the lowest score.

        :raises StopIteration: if there are no values to return.
        """
        return self._pop(reverse=False)

    def rpop(self):
        """Pop a single element which has the highest score.

        :raises StopIteration: if there are no values to return.
        """
        return self._pop(reverse=True)

    def pop_many(self, score_threshold, /) -> list:
        """Pop and return values with scores less than `score_threshold`.

        The returned values are guaranteed to be in order.
        Returns an empty list if no values.
        """
        return self._pop_many(score_threshold, reverse=False)

    def rpop_many(self, score_threshold, /) -> list:
        """Pop and return values with scores greater than `score_threshold`.

        Returned values are guaranteed to be in order.
        """
        return self._pop_many(score_threshold, reverse=True)

    def clear(self):
        """Clear all values."""
        self._scores.clear()
        self._values.clear()

    def _pop_many(self, score_threshold, reverse=False) -> list:
        """Pop values with scores less than `score`.

        The returned values are guaranteed to be in order.
        Returns an empty list if no values.
        """
        idx = bisect(self._scores, score_threshold)
        if reverse:
            self._scores = self._scores[:idx]
            values, self._values = self._values[idx:], self._values[:idx]
        else:
            self._scores = self._scores[idx:]
            values, self._values = self._values[:idx], self._values[idx:]
        return values

    def _pop(self, reverse=False):
        if not self._values:
            raise StopIteration('Empty stack.')
        if reverse:
            del self._scores[-1]
            return self._values.pop(-1)
        else:
            del self._scores[0]
            return self._values.pop(0)

    def _select(self, score_threshold, reverse=False) -> list:
        """Select and return items without removing them from the stack.

        The values are guaranteed to be in order.
        """
        idx = bisect(self._scores, score_threshold)
        if reverse:
            values = self._values[idx:]
            values.reverse()
            return values
        else:
            return self._values[:idx]


class RestrictedDict(dict):
    """Same as a normal mapping but forbids key updates.

    >>> m = RestrictedDict(a=1, b=2)
    >>> m['c'] = 3
    >>> 'c' in m
    True

    Resetting a key raises a ValueError:

    >>> m['c'] = 5  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError:

    >>> m.update({'c': 5})   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    NotImplementedError:

    So as trying to remove it:

    >>> m.pop('c')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    NotImplementedError:

    """

    __msg = 'Restricted mapping does not allow key deletion.'

    @not_implemented(__msg)
    def popitem(self):
        ...

    @not_implemented(__msg)
    def pop(self, __key):
        ...

    @not_implemented(__msg)
    def update(self, __m, **kwargs):
        ...

    def __setitem__(self, __k, __v) -> None:
        if self.__contains__(__k):
            raise ValueError('Item is already present.')
        super().__setitem__(__k, __v)


NSKey = NewType('NSKey', str)  # namespace key


@dataclass
class Namespace(Mapping):
    """Namespace can be used for shared key and name management."""

    delimiter = '.'  # it is supported both by kafka topics and redis keys

    env: str
    name: str
    namespaces: Dict[str, 'Namespace'] = field(init=False, default_factory=RestrictedDict)

    def get_key(self, __key: str) -> NSKey:
        """Get a shared key."""
        if self.delimiter in __key:
            raise ValueError(f'"{self.delimiter}" symbol is not allowed in namespace names.')
        return cast(NSKey, self.delimiter.join((self.env, self.name, __key)))

    def create_namespace(self, __ns: str) -> 'Namespace':
        """Create a new sub-namespace."""
        if self.delimiter in __ns:
            raise ValueError(f'"{self.delimiter}" symbol is not allowed in namespace names.')
        ns = Namespace(env=self.env, name=self.delimiter.join((self.name, __ns)))
        self.namespaces[ns.name] = ns
        return ns

    def __getitem__(self, __item: str) -> 'Namespace':
        return self.namespaces[__item]

    def __len__(self):
        return len(self.namespaces)

    def __iter__(self) -> Iterator[str]:
        return iter(self.namespaces)

    def __truediv__(self, __other: str) -> 'Namespace':
        return self.create_namespace(__other)

    def __str__(self):
        return self.delimiter.join((self.env, self.name))


class TTLDict(MutableMapping):
    """A simple TTL dict mostly compatible with a normal one."""

    TTL = 60  #: default TTL in ms
    __slots__ = ('_ttl', '_dict', '_ttls', '_keys')

    def __init__(self, *args, **kws):
        self._ttl = int(self.TTL)
        self._dict = dict()  # here key: (value, index) data will be stored
        self._keys = []  # sorted list of keys
        self._ttls = []  # sorted list of deadlines
        for key, value in dict(*args, **kws).items():
            self[key] = value

    def __getitem__(self, key):
        value = self._dict[key]
        n = self._keys.index(key)
        t = self._ttls[n]
        if t > time():
            return value
        else:
            del self[key]
            raise KeyError(key)

    def __setitem__(self, key, value):
        return self.set(key, value, self._ttl)

    def __delitem__(self, key):
        n = self._keys.index(key)
        del self._keys[n]
        del self._ttls[n]
        del self._dict[key]

    def __len__(self):
        self.refresh()
        return len(self._dict)

    def __bool__(self):
        return bool(len(self))

    def __contains__(self, item):
        return self.get(item) is not None

    def __eq__(self, other):
        self.refresh()
        other.refresh()
        return other._dict == self._dict  # noqa

    def __iter__(self):
        return iter(self.keys())

    def get(self, item, default=None):
        """Similar to `dict().get`."""
        try:
            return self[item]
        except KeyError:
            return default

    def set(self, key, value, ttl: int):
        """Set key.

        Similar to `__setitem__` but you may specify per-key ttl.
        """
        if key in self._dict:
            del self[key]
            self.set(key, value, ttl)
        else:
            if ttl:
                t = int(time() + ttl)
            else:
                t = cast(int, float('Inf'))
            n = bisect_left(self._ttls, t)
            self._ttls.insert(n, t)
            self._keys.insert(n, key)
            self._dict[key] = value

    def values(self):
        """Similar to `dict().values`."""
        self.refresh()
        return self._dict.values()

    def keys(self):
        """Similar to `dict().keys`."""
        self.refresh()
        return self._dict.keys()

    def items(self):
        """Similar to `dict().items`."""
        return zip(self._dict.keys(), self.values())

    def set_ttl(self, ttl: int):
        """Set default ttl to a new value.

        :param ttl: TTL value in seconds
        """
        if not ttl:
            ttl = sys.maxsize
        elif ttl < 0:
            raise ValueError('TTL value must be greater than zero.')
        ttl = int(ttl)
        self._ttl = ttl

    def refresh(self):
        """Remove old records.

        .. note::

            This method is called each time one calls a `TTLDict.__len__`
            or any other method that must provide an actual dictionary state.

        """
        t = int(time())
        n = bisect_right(self._ttls, t)
        if n:
            self._ttls = self._ttls[n:]
            keys, self._keys = self._keys[:n], self._keys[n:]
            for key in keys:
                del self._dict[key]


REQUEST_CONTEXT: ContextVar[Optional[RequestContext]] = ContextVar('RequestContext', default=None)
REQUEST_SESSION: ContextVar[Optional[Session]] = ContextVar('RequestSession', default=None)
