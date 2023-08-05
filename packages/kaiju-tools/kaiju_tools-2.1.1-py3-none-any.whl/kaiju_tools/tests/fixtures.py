import asyncio
import gc
import logging
import multiprocessing as mp
import os
import platform
import queue
import signal
import traceback
import uuid
from datetime import timedelta, datetime
from inspect import iscoroutinefunction
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
from time import sleep
from types import SimpleNamespace
from typing import *

import pytest

import kaiju_tools.jsonschema as j
from kaiju_tools.rpc import AbstractRPCCompatible, JSONRPCServer
from kaiju_tools.services import Service, ServiceContextManager
from kaiju_tools.logging import Logger
from kaiju_tools.exceptions import ValidationError

__all__ = ('logger', 'application', 'temp_dir', 'sample_file', 'rpc_interface', 'rpc_compatible_service')


@pytest.fixture(scope='session')
def logger():
    """Return a test logger preconfigured to DEBUG level."""
    logger = logging.getLogger('pytest')
    logger.setLevel('DEBUG')
    return logger


@pytest.fixture
def application(logger):
    """Return a sample aiohttp web app object to use in tests. Requires aiohttp.

    You may pass a list of `Service` classes. They won't be initialized but they will be registered
    in the pseudo-service context meaning you can use `app.services.<service_name>` inside you code
    as if it's a normal initialized app.
    """
    from aiohttp.web import Application

    def _application(*services: Service, name='pytest', id=str(uuid.uuid4()), **kws):
        app = Application(logger=logger, **kws)
        app['id'] = app.id = id
        app['name'] = app.name = name
        app['env'] = app.env = 'dev'
        app.services = ServiceContextManager(app, settings=[])  # noqa
        for service in services:
            service.app = app
        app.services._services = {service.service_name: service for service in services}
        app.services._create_services = lambda: None
        return app

    return _application


@pytest.fixture
def temp_dir():
    with TemporaryDirectory(prefix='pytest') as d:
        yield Path(d)


@pytest.fixture
def sample_file():
    with NamedTemporaryFile(prefix='pytest', delete=False) as f:
        name = f.name
        f.write('test')
    yield Path(name)
    os.remove(name)


@pytest.fixture
def rpc_interface(application, logger):
    app = application(debug=True)
    return JSONRPCServer(app=app, session_service=False, logger=logger)


@pytest.fixture
def rpc_compatible_service():
    class TestService(Service, AbstractRPCCompatible):
        service_name = 'm'

        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            self.retry_counter = 0

        @property
        def validators(self) -> dict:
            return {'validated': j.Object({'a': j.Integer(), 'b': j.Integer()}, required=['a', 'b'])}

        @property
        def permissions(self) -> Optional[dict]:
            return {
                '*': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
                'method_with_user_permission': self.PermissionKeys.GLOBAL_USER_PERMISSION,
                'method_with_user_permission_2': self.PermissionKeys.GLOBAL_USER_PERMISSION,
            }

        @property
        def routes(self) -> dict:
            return {
                'echo': self.echo,
                'aecho': self.async_echo,
                'sum': self.sum,
                'fail': self.failed,
                'long_echo': self.async_long_echo,
                'split': self.split,
                'standard_echo': self.async_standard_echo,
                'validated': self.validated_method,
                'uses_context': self.uses_context,
                'method_with_user_permission': self.echo_true,
                'method_with_user_permission_2': self.echo_true,
                'method_with_retry': self.retry_method,
            }

        async def retry_method(self, when: int) -> bool:
            self.retry_counter += 1
            if self.retry_counter < when:
                raise TimeoutError('Simulated timeout')
            self.retry_counter = 0
            return True

        async def echo_true(self, *args, **kws):
            return True

        async def uses_context(self):
            """Check if a session matches the context."""
            return await self._uses_context()

        async def _uses_context(self):
            await asyncio.sleep(0.1)
            stored_session = self.get_session()
            return stored_session

        async def sum(self, x: float, y: float) -> float:
            """Sum something.

            :param x: first value
            :example x: 7
            :param y: second value
            :example y: 6
            :returns: sum of two values
            """
            return x + y

        async def split(self, value: str, delimiter: str) -> List[str]:
            """Split a string value by delimiter.

            :returns: split parts
            """
            return value.split(delimiter)

        async def failed(self):
            """Do wrong command."""
            raise ValueError('Something bad happened.')

        async def echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing echo.')
            return args, kws

        async def async_echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing async echo.')
            await asyncio.sleep(0.01)
            return args, kws

        async def async_standard_echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing echo.')
            await asyncio.sleep(0.01)
            return args, kws

        async def async_long_echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing long echo.')
            await asyncio.sleep(2.2)
            return args, kws

        async def validated_method(self, a: int, b: int):
            """Call a method with a validated input."""
            return a * b

    return TestService
