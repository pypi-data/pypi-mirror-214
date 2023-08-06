from random import choices
from string import hexdigits
from typing import TypeVar, Type, Optional, cast, Any, TYPE_CHECKING

from tortoise import timezone

from fastapi_all_out.auth.user_service import BaseUserService, UNUSED_PASSWORD_PREFIX
from fastapi_all_out.lazy_objects import get_global_objects
from fastapi_all_out.enums import TempCodeTriggers
from .models import BaseUser, max_len_of, get_field_param

if TYPE_CHECKING:
    from .models.temp_code import TempCode


USER_MODEL = TypeVar("USER_MODEL", bound=BaseUser)
UserModel = cast(Type[BaseUser], get_global_objects().USER_MODEL)


class TortoiseUserService(BaseUserService[USER_MODEL]):
    _temp_code_model: Type["TempCode"]

    def set_password(self, password: Optional[str]) -> None:
        user = self.user
        user.password_change_dt = timezone.now()
        user.password_salt = ''.join(choices(hexdigits, k=max_len_of(UserModel)('password_salt')))
        if password:
            user.password_hash = self.get_password_hash(password)
        else:
            user.password_hash = UNUSED_PASSWORD_PREFIX + self.get_password_hash(''.join(choices(hexdigits, k=30)))

    async def update_password(self, password: str) -> None:
        self.set_password(password)
        await self.user.save(force_update=True, update_fields=['password_hash', 'password_change_dt', 'password_salt'])

    @classmethod
    def get_temp_code_model(cls) -> Type["TempCode"]:
        if not hasattr(cls, '_temp_code_model'):
            cls._temp_code_model = get_field_param(UserModel, 'temp_code', 'related_model')
        return cls._temp_code_model

    async def create_temp_code(
            self, trigger: TempCodeTriggers, extras: dict[str, Any] | list[Any] = None
    ) -> "TempCode":
        return await self.get_temp_code_model().new(user=self.user, trigger=trigger, extras=extras)

    async def get_temp_code(
            self, trigger: TempCodeTriggers
    ) -> Optional["TempCode"]:
        return await self.get_temp_code_model().get_or_none(user=self.user, trigger=trigger)

    async def update_temp_code(
            self, temp_code: "TempCode", extras: dict[str, Any] | list[Any] = None
    ) -> None:
        await temp_code.update(extras=extras)

    async def delete_temp_code(
            self, temp_code: "TempCode"
    ) -> None:
        await temp_code.delete()
