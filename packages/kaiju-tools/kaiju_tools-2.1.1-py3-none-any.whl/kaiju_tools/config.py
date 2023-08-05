"""Application configuration and CLI options."""

import logging
import os
import pathlib
import yaml
from ast import literal_eval
from argparse import ArgumentParser
from functools import partial
from warnings import warn
from typing import Iterable

import kaiju_tools.jsonschema as js
from kaiju_tools.serialization import load
from kaiju_tools.mapping import recursive_update
from kaiju_tools.templates import Template

__all__ = (
    'ConfigLoader',
    'get_cli_parser',
    'ConfigurationError',
    'Settings',
    'AppSettings',
    'RunSettings',
    'ProjectSettings',
    'MainSettings',
    'ServiceSettings',
)


class ConfigurationError(KeyError):
    """Configuration key not found."""


class Settings(dict):
    """Settings object."""

    validator: js.Object = None

    def __init__(self, seq):
        """Initialize."""
        if self.validator:
            seq = js.compile_schema(self.validator)(seq)
        super().__init__(seq)

    def __getattr__(self, item):
        """Get a parameter from settings dict."""
        try:
            return self[item]
        except KeyError:
            raise ConfigurationError(f'No such config value: {item}')


class AppSettings(Settings):
    """Web application init settings."""

    validator = js.Object(
        {'debug': js.Boolean(default=False), 'client_max_size': js.Integer(minimum=1024, default=1024**2)},
        additionalProperties=False,
        required=[],
    )


class RunSettings(Settings):
    """Server run settings."""

    validator = js.Object(
        {
            'host': js.Nullable(js.String(minLength=1, default=None)),
            'port': js.Nullable(js.Integer(minimum=1, maximum=65535, default=None)),
            'path': js.Nullable(js.String(minLength=1, default=None)),
            'shutdown_timeout': js.Integer(minimum=0, default=30),
            'keepalive_timeout': js.Integer(minimum=0, default=60),
        },
        additionalProperties=False,
        required=[],
    )


class MainSettings(Settings):
    """Main project settings."""

    validator = js.Object(
        {
            'name': js.String(minLength=1),
            'version': js.String(minLength=1),
            'env': js.String(minLength=1),
            'loglevel': js.Enumerated(enum=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO'),
        },
        additionalProperties=False,
        required=['name', 'version', 'env'],
    )


class ServiceSettings(Settings):
    """Service configuration."""

    validator = js.Object(
        {
            'cls': js.String(minLength=1),
            'name': js.String(minLength=1),
            'enabled': js.Boolean(default=True),
            'required': js.Boolean(default=True),
            'override': js.Boolean(default=False),
            'loglevel': js.JSONSchemaObject(enum=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default=None),
            'settings': js.Object(),
        },
        additionalProperties=False,
        required=['cls'],
    )

    def __init__(self, seq):
        if type(seq) is str:
            seq = {'cls': seq}
        super().__init__(seq)


class ProjectSettings(Settings):
    """Validation schema for project settings."""

    def __init__(self, app, run, main, etc, services):
        """Initialize."""
        super().__init__(
            dict(
                app=AppSettings(app),
                run=RunSettings(run),
                main=MainSettings(main),
                etc=Settings(etc),
                services=tuple(ServiceSettings(srv) for srv in services),
            )
        )


def get_cli_parser() -> ArgumentParser:
    """Parse application init args."""
    _parser = ArgumentParser(prog='aiohttp web application', description='web application run settings')
    _parser.add_argument('--host', dest='host', default=None, help='web app host (default - from settings)')
    _parser.add_argument('--port', dest='port', type=int, default=None, help='web app port (default - from settings)')
    _parser.add_argument(
        '--path', dest='path', default=None, metavar='FILE', help='socket path (default - from settings)'
    )
    _parser.add_argument(
        '--debug', dest='debug', action='store_true', default=None, help='run in debug mode (default - from settings)'
    )
    _parser.add_argument(
        '-c',
        '--config',
        dest='cfg',
        default=[],
        metavar='FILE',
        action='append',
        help='yaml config paths, use multiple times to merge multiple configs (default - settings/config.yml)',
    )
    _parser.add_argument(
        '-l',
        '--log',
        dest='loglevel',
        default=None,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='log level',
    )
    _parser.add_argument(
        '-f',
        '--env-file',
        dest='env_file',
        default=[],
        metavar='FILE',
        action='append',
        help='env file paths (default to ./settings/env.json + ./settings/env.local.json)',
    )
    _parser.add_argument(
        '-e',
        '--env',
        dest='env',
        default=[],
        metavar='KEY=VALUE',
        action='append',
        help='overrides env variable (may be used multiple times)',
    )
    _parser.add_argument(
        '--no-os-env', dest='no_os_env', action='store_true', default=False, help='do not use OS environment variables'
    )
    _parser.add_argument(
        'cmd', metavar='COMMAND', default=None, nargs='?', help='optional management command to execute'
    )
    return _parser


class ConfigLoader:
    """Config loader class. It is intended to be used before the app start."""

    config_class = ProjectSettings
    _file_loaders = {
        '.json': load,
        '.yml': partial(yaml.load, Loader=yaml.SafeLoader),
        '.yaml': partial(yaml.load, Loader=yaml.SafeLoader),
    }

    def __init__(
        self,
        base_config_paths: Iterable[str] = tuple(),
        base_env_paths: Iterable[str] = tuple(),
        default_env_paths: Iterable[str] = tuple(),
    ):
        """Initialize.

        :param base_config_paths: list of base config files in yaml format, all other config files are appended to the
            end of this list
        :param base_env_paths: list of base env files in json format, all other env files are appended to the end of
            this list
        :param default_env_paths: list of default env files in json format
        """
        self.base_config_paths = base_config_paths
        self.base_env_paths = base_env_paths
        self.default_env_paths = default_env_paths
        self.logger = logging.getLogger('loader')

    def configure(self) -> (str, ProjectSettings):
        """Load project config and command.

        Loading order:

        - ./settings/config.yml
        - .yml files, first to last
        - ./settings/env.json
        - .env files, first to last
        - os env vars (unless --no-os-env specified)
        - CLI env vars

        """
        parser = get_cli_parser()
        args = parser.parse_known_args()[0].__dict__
        config_paths = [*self.base_config_paths, *args.get('cfg', [])]
        _paths = args.get('env_file', [])
        if not _paths:
            _paths = self.default_env_paths
        env_paths = [*self.base_env_paths, *_paths]
        config, env = {}, {}
        for cfg_path in config_paths:
            _data = self._from_file(cfg_path)
            _services = _data.pop('services', [])
            config = recursive_update(config, _data)
            if 'services' in config:
                config['services'].extend(_services)
            else:
                config['services'] = _services
        for env_path in env_paths:
            env.update(self._from_file(env_path))
        if not args['no_os_env']:
            self._update_env_from_os(env)
        self._update_env_from_cli(env, args)
        config = self._from_dict(config, env)
        if not args['no_os_env']:
            self._update_config_from_os(config)
        self._update_config_from_cli(config, args)
        command = args.get('cmd')
        config = ProjectSettings(**config)
        return command, config

    def _from_file(self, path) -> dict:
        """Load data from a config file."""
        self.logger.info('Loading %s', path)
        path = pathlib.Path(path)
        if path.suffix not in self._file_loaders:
            raise ConfigurationError(f'Unknown config file format: {path}')
        loader = self._file_loaders[path.suffix]
        if not path.exists() or path.is_dir():
            warn('Config path does not exist or it\'s a directory.' ' "%s" - not found!' % path)
            return {}
        with open(path) as f:
            data = loader(f)
        return data

    def _from_dict(self, data: dict, env: dict) -> ProjectSettings:
        """Create config from a template and env map."""
        data = Template(data).fill(env)
        config = self.config_class(**data)
        return config

    def _update_env_from_os(self, env: dict) -> None:
        """Get env arguments from OS env."""
        self.logger.debug('Loading OS')
        for key in list(env.keys()):
            value = os.getenv(key)
            if value:
                self.logger.info('From OS: %s', key)
                env[key] = self._init_env_value(value)

    def _update_env_from_cli(self, env: dict, args: dict) -> None:
        """Update env map from CLI arguments."""
        self.logger.debug('Loading CLI')
        for record in args.get('env', []):
            k, v = record.split('=')
            if v:
                self.logger.info('From CLI: %s', k)
                env[k] = self._init_env_value(v)

    def _update_config_from_os(self, config: ProjectSettings):
        """Set OS args."""

    @staticmethod
    def _update_config_from_cli(config: ProjectSettings, args: dict):
        """Set CLI arguments."""
        for key in ('host', 'port', 'path'):
            value = args.get(key)
            if value is not None:
                config.run[key] = value
        debug = args.get('debug')
        if debug is not None:
            config.app['debug'] = debug
        log = args.get('loglevel')
        if log is not None:
            config.main['loglevel'] = log

    @staticmethod
    def _init_env_value(value: str):
        """Parse env arg from --env or unix environment."""
        if value is None:
            return None
        value = value.strip()
        if not value:
            return None
        _value = value.lower()
        if _value == 'true':
            value = True
        elif _value == 'false':
            value = False
        elif _value == 'none':
            value = None
        else:
            try:
                value = literal_eval(value)
            except Exception:  # noqa that's ok in eval
                pass
        return value
