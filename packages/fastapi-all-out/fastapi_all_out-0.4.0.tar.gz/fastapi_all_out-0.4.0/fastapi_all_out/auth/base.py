from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Callable, Coroutine, Any, Optional, Protocol, Self
from uuid import UUID

from fastapi import APIRouter

from fastapi_all_out.enums import TempCodeTriggers
from fastapi_all_out.pydantic import ConfigModel


class AuthStrategy(ABC):
    authorize_response_model: Any

    def authorize(self, user: "BaseUser") -> Any: ...

    @classmethod
    @abstractmethod
    def from_config(cls, config: ConfigModel) -> Self: ...


class AuthBackend(ABC):

    strategy: "AuthStrategy"

    def __init__(self, strategy: "AuthStrategy"):
        self.strategy = strategy

    def authorize(self, user: "BaseUser") -> Any:
        return self.strategy.authorize(user=user)

    @classmethod
    @abstractmethod
    def from_config(cls, strategy: AuthStrategy, config: ConfigModel) -> Self: ...

    @abstractmethod
    def authenticate_dependency(self) -> Callable[[], Coroutine[Any, Any, None]]: ...

    @abstractmethod
    def auth_required_dependency(self) -> Callable[[], Coroutine[Any, Any, None]]: ...

    @abstractmethod
    def load_user_dependency(self) -> Callable[[], Coroutine[Any, Any, None]]: ...

    @abstractmethod
    def load_user_optionally_dependency(self) -> Callable[[], Coroutine[Any, Any, None]]: ...

    @abstractmethod
    def with_permissions_dependency(self, *permissions: tuple[str, str]) -> Callable[[], Coroutine[Any, Any, None]]: ...

    def create_router(self, add_login_route: bool = True, add_logout_route: bool = True, **kwargs) -> APIRouter:
        kwargs.setdefault('prefix', '/auth/jwt')
        kwargs.setdefault('tags', ['auth'])
        router = APIRouter(**kwargs)
        if add_login_route:
            self.add_login_route(router)
        if add_logout_route:
            self.add_logout_route(router)
        return router

    @abstractmethod
    def add_login_route(self, router: APIRouter) -> None: ...

    @abstractmethod
    def add_logout_route(self, router: APIRouter) -> None: ...


class AuthConfig(ConfigModel):
    backend: str
    strategy: str


class BaseUser:
    id: int
    uuid: UUID
    username: Optional[str]
    email: Optional[str]
    password_hash: str
    password_change_dt: datetime
    password_salt: str
    is_superuser: bool
    is_active: bool
    created_at: datetime
    EMAIL_FIELD: str
    AUTH_FIELDS: tuple[str, ...]

    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    @property
    def display_name(self) -> str:
        raise NotImplementedError()

    @property
    def is_simple(self) -> bool:
        raise NotImplementedError()

    def has_permissions(self, *permissions) -> tuple[str, str]:
        raise NotImplementedError()


class SimpleUser(BaseUser):
    pk: Any

    def __init__(self, pk: int | UUID | str, username: str, **kwargs):
        self.pk = pk
        self.username = username
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def is_simple(self) -> bool:
        return True


class UnauthenticatedUser(BaseUser):
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ""

    def is_simple(self) -> bool:
        return True


class TempCodeProto(Protocol):
    code: str
    expired_at: datetime
    trigger: TempCodeTriggers
    extras: Optional[dict[str, Any] | list[Any]]

    @property
    def duration(self) -> timedelta: ...

    @property
    def is_expired(self) -> bool: ...
