from importlib import import_module
from typing import TypeVar, Generic, TYPE_CHECKING, Type, Any
from inspect import isclass

from pydantic.utils import import_string

from fastapi_all_out.enums import Databases

if TYPE_CHECKING:
    from fastapi_all_out.settings import BaseSettings
    from fastapi_all_out.code_responses import DefaultCodes
    from fastapi_all_out.routers.base_repository import BaseRepository, BaseUserRepository
    from fastapi_all_out.auth.user_service import BaseUserService
    from fastapi_all_out.auth.base import AuthBackend, AuthStrategy, BaseUser
    from fastapi_all_out.mailing import MailSender


_T = TypeVar("_T")


class LazyObject(Generic[_T]):
    lazy_obj_path: str
    lazy_obj: _T
    init: bool

    def __init__(self, lazy_obj_path: str, *, init: bool = False):
        self.lazy_obj_path = lazy_obj_path
        self.init = init

    def _make_import(self, instance: "DefaultGlobalObjects") -> _T | Type[_T]:
        return import_string(self.lazy_obj_path)

    def _get_object(self, instance: "DefaultGlobalObjects") -> _T | Type[_T]:
        obj = self._make_import(instance)
        if self.init:
            assert isclass(obj), f'{obj} must be a class'
            obj = self._init_object(obj, instance=instance)
        return obj

    def _init_object(self, obj: Type[_T], instance: "DefaultGlobalObjects") -> _T:
        return obj()

    def __get__(self, instance: "DefaultGlobalObjects", owner: Type["DefaultGlobalObjects"]) -> _T:
        if not hasattr(self, 'lazy_obj'):
            self.lazy_obj = self._get_object(instance)
        return self.lazy_obj

    def __set__(self, instance: "DefaultGlobalObjects", value: str) -> None:
        raise Exception('Read only')


class LazyObjectAuthDB(LazyObject[_T]):
    def _make_import(self, instance: "DefaultGlobalObjects") -> _T:
        db = instance.auth_db.value
        return import_string(self.lazy_obj_path.format(db, db.title()))


class LazyAuthBackend(LazyObject["AuthBackend"]):

    def __init__(self, lazy_obj_path: str):
        super().__init__(lazy_obj_path, init=True)

    def _init_object(self, obj: Type["AuthBackend"], instance: "DefaultGlobalObjects") -> "AuthBackend":
        return obj.from_config(strategy=instance.AUTH_STRATEGY, config=get_settings().get_auth_config())


class LazyAuthStrategy(LazyObject["AuthStrategy"]):

    def __init__(self, lazy_obj_path: str):
        super().__init__(lazy_obj_path, init=True)

    def _init_object(self, obj: Type["AuthStrategy"], instance: "DefaultGlobalObjects") -> "AuthStrategy":
        return obj.from_config(config=get_settings().get_auth_config())


class LazyUserModel(LazyObject["BaseUser"]):
    def __init__(self):
        #  set owner class
        super().__init__('')

    def _make_import(self, instance: "DefaultGlobalObjects") -> "BaseUser":
        return import_string(instance.user_model_path)


class LazyMailSender(LazyObject["MailSender"]):
    def _make_import(self, instance: "DefaultGlobalObjects") -> "MailSender":
        return super()._make_import(instance=instance)(conf=get_settings().get_mailing_config)


class DefaultGlobalObjects:

    auth_db: Databases = Databases.tortoise
    user_model_path = 'models.User'

    CODES: Type["DefaultCodes"] = LazyObject('fastapi_all_out.code_responses.DefaultCodes')

    REPOSITORY: Type["BaseRepository"] = \
        LazyObjectAuthDB('fastapi_all_out.contrib.{}.repository.{}Repository')
    USER_REPOSITORY: Type["BaseUserRepository"] = \
        LazyObjectAuthDB('fastapi_all_out.contrib.{}.user_repository.{}UserRepository')
    USER_SERVICE: Type["BaseUserService"] = \
        LazyObjectAuthDB('fastapi_all_out.contrib.{}.user_service.{}UserService')
    USER_MODEL: Type["BaseUser"] = LazyUserModel()
    AUTH_BACKEND: "AuthBackend" = LazyAuthBackend('fastapi_all_out.auth.jwt.backend.JWTOAuth2PasswordBearerBackend')
    AUTH_STRATEGY: "AuthStrategy" = LazyAuthStrategy('fastapi_all_out.auth.jwt.strategy.RS256JWTAuthStrategy')

    MAIL_SENDER: "MailSender" = LazyObject('fastapi_all_out.mailing.mail_sender')


def get_settings_var(var: str, default: Any = '__undefined__') -> Any:
    settings = import_module('settings')
    if default == '__undefined__':
        return getattr(settings, var)
    return getattr(settings, var, default)


def get_settings() -> "BaseSettings":
    return get_settings_var('settings')


def get_global_objects() -> DefaultGlobalObjects:
    return import_string('global_objects.global_objects')


def get_schema(default: Type[_T], field: bool = False) -> Type[_T]:
    prefix = 'fields' if field else 'schemas'
    try:
        return import_string(f'{prefix}.{default.__name__}')
    except ImportError as e:
        try:
            if not get_settings_var('PROD'):
                print(e)
        except AttributeError:
            pass
        return default
