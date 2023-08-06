from typing import TypeVar, Any, Generic, Literal, Optional, TYPE_CHECKING, Sequence
from abc import ABC, abstractmethod

from passlib.context import CryptContext
from fastapi import Request, BackgroundTasks, Response

from fastapi_all_out.enums import TempCodeTriggers
from fastapi_all_out.lazy_objects import get_global_objects
from fastapi_all_out.code_responses import BaseCodes
from .base import BaseUser

if TYPE_CHECKING:
    from fastapi_all_out.auth.base import TempCodeProto


USER_MODEL = TypeVar("USER_MODEL", BaseUser, Any)
UNUSED_PASSWORD_PREFIX = '!'
gl = get_global_objects()


class BaseUserService(Generic[USER_MODEL], ABC):

    user: USER_MODEL
    pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

    def __init__(self, user: USER_MODEL):
        self.user = user

    def can_login(self) -> bool:
        return self.user.is_active

    async def if_cant_login(self, request: Request, background_tasks: BackgroundTasks, response: Response) -> None:
        pass

    def token_expired(self, iat: int) -> bool:
        return self.user.password_change_dt.timestamp() > iat

    @abstractmethod
    def set_password(self, password: str) -> None: ...

    @abstractmethod
    async def update_password(self, password: str) -> None: ...

    def get_fake_password(self, password: str) -> str:
        return password + str(self.user.password_change_dt.timestamp()) + self.user.password_salt

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(self.get_fake_password(password))

    def verify_password(self, password: str) -> bool:
        if self.user.password_hash.startswith(UNUSED_PASSWORD_PREFIX):
            return False
        return self.pwd_context.verify(self.get_fake_password(password), self.user.password_hash)

    async def post_registration(self, request: Request, background_tasks: BackgroundTasks, response: Response) -> None:
        background_tasks.add_task(self.send_activation_email)

    async def send_activation_email(self) -> None:
        temp_code = await self.update_or_create_temp_code(trigger=TempCodeTriggers.EmailActivation)
        await gl.MAIL_SENDER.activation_email(user=self.user, temp_code=temp_code)

    async def send_email_change_email(self, new_email: str) -> None:
        temp_code = await self.update_or_create_temp_code(
            trigger=TempCodeTriggers.EmailChange, extras={'new_email': new_email}
        )
        await gl.MAIL_SENDER.email_change_email(user=self.user, temp_code=temp_code, new_email=new_email)

    async def send_password_reset_email(self) -> None:
        temp_code = await self.update_or_create_temp_code(trigger=TempCodeTriggers.PasswordReset)
        await gl.MAIL_SENDER.password_reset_email(user=self.user, temp_code=temp_code)

    @abstractmethod
    async def create_temp_code(
            self, trigger: TempCodeTriggers, extras: dict[str, Any] | list[Any] = None
    ) -> "TempCodeProto": ...

    @abstractmethod
    async def get_temp_code(
            self, trigger: TempCodeTriggers
    ) -> Optional["TempCodeProto"]: ...

    @abstractmethod
    async def update_temp_code(
            self, temp_code: "TempCodeProto", extras: dict[str, Any] | list[Any] = None
    ) -> None: ...

    @abstractmethod
    async def delete_temp_code(
            self, temp_code: "TempCodeProto"
    ) -> None: ...

    async def update_or_create_temp_code(
            self, trigger: TempCodeTriggers, extras: dict[str, Any] | list[Any] = None
    ) -> "TempCodeProto":
        temp_code = await self.get_temp_code(trigger=trigger)
        if temp_code:
            await self.update_temp_code(temp_code, extras=extras)
            return temp_code
        else:
            return await self.create_temp_code(trigger=trigger, extras=extras)

    @classmethod
    def check_temp_code_error(
            cls,
            code: str,
            temp_code: "TempCodeProto",
    ) -> Literal['expired', 'incorrect'] | None:
        if temp_code.is_expired:
            return 'expired'
        if temp_code.code != code:
            return 'incorrect'

    async def raise_if_cant_change_email(self, new_email: str) -> bool:
        pass

    @classmethod
    def cant_change_email_responses(cls) -> Sequence[BaseCodes | tuple["BaseCodes", dict[str, Any]]]:
        return ()
