import os
from typing import TYPE_CHECKING, Any
from pathlib import Path

from pydantic import BaseSettings as PydanticBaseSettings, AnyHttpUrl


if TYPE_CHECKING:
    from fastapi_all_out.pydantic import ConfigModel
    from fastapi_all_out.db_connection import EmptyDatabasesConfig
    from fastapi_all_out.mailing import MailingConfig


def any_env_exists(*filenames: str) -> Path | None:
    for filename in reversed(filenames):
        _p = BASE_PATH / filename
        if _p.exists():
            return _p


BASE_PATH = Path().resolve()

if env_file := any_env_exists('production.env'):
    MODE = 'PROD'
elif env_file := any_env_exists('dev.env'):
    MODE = 'DEV'
elif env_file := any_env_exists('.env', 'debug.env'):
    MODE = 'DEBUG'
else:
    MODE = os.environ.get('MODE') or 'DEBUG'
    env_file = None

DEBUG, DEV, PROD = MODE == 'DEBUG', MODE == 'DEV', MODE == 'PROD'


class BaseSettings(PydanticBaseSettings):

    API_PREFIX: str = '/api'

    class Config(PydanticBaseSettings.Config):
        env_file = env_file
        env_nested_delimiter = '__'

    def _get_inner_config(self, attr: str) -> Any:
        if not hasattr(self, attr):
            raise Exception(f'set `{attr}` attribute to your settings or override `get_{attr}_config`')
        return getattr(self, attr)

    def get_mailing_config(self) -> "MailingConfig":
        return self._get_inner_config('mailing')

    def get_auth_config(self) -> "ConfigModel":
        return self._get_inner_config('auth')

    def get_db_config(self) -> "EmptyDatabasesConfig":
        return self._get_inner_config('db')
