from typing import Type, Any

from fastapi_all_out.lazy_objects import get_global_objects
from .repository import TortoiseRepository
from .user_service import USER_MODEL
from ...routers.base_repository import ModelPrefix, BaseUserRepository


global_objects = get_global_objects()
UserService = global_objects.USER_SERVICE


class TortoiseUserRepository(TortoiseRepository[USER_MODEL], BaseUserRepository[USER_MODEL]):
    model: Type[USER_MODEL] = global_objects.USER_MODEL

    pass_check_required: dict[str, set[str]] = {'': {'password_hash', 'password_change_dt', 'password_salt'}}

    async def handle_create_(
            self,
            model: Type[USER_MODEL],
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
            defaults: dict[str, Any] = None,
            commit: bool = True,
    ) -> USER_MODEL:
        password = data.pop('password')
        user = await self._handle_create_default(
            model=model,
            data=data,
            exclude=exclude,
            prefix=prefix,
            defaults=defaults,
            commit=False,
        )
        UserService(user).set_password(password)
        if commit:
            await user.save(force_create=True)
        return user

    async def create_superuser(self, data: dict[str, Any]) -> None:
        print(data)
        await self.create(data, defaults={'is_superuser': True, 'is_active': True})

    @classmethod
    def get_create_superuser_fields(cls) -> tuple[str, ...]:
        return 'username', 'email', 'password', 're_password'
