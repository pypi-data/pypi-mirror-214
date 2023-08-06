from datetime import datetime
from typing import Any, Optional

from pydantic import root_validator, validator, EmailStr, Field

from fastapi_all_out.pydantic import CamelModel, Password, Username, RelatedList, CamelModelORM
from fastapi_all_out.models import max_len_of
from fastapi_all_out.lazy_objects import get_global_objects, get_schema
from fastapi_all_out.schemas import PermissionRead


__all__ = [
    "PasswordsPair", "ChangePassword", "BaseLoginPasswordSchema", "LoginPasswordSchema",
    "UserRead", "UserMeRead", "UserEdit", "UserMeEdit", "UserCreate", "UserRegistration",
]

UserModel = get_global_objects().USER_MODEL
Username = get_schema(Username, field=True)
Password = get_schema(Password, field=True)


class PasswordsPair(CamelModel):
    password: Password
    re_password: str

    @validator('re_password')
    def passwords_equal(cls, v: str, values: dict[str, Any]):
        if pw := values.get('password'):
            if v != pw:
                raise ValueError("passwordsMismatch")
        return v


class BaseLoginPasswordSchema(CamelModel):
    login: Optional[str]
    password: str

    @root_validator
    def what_is(cls, values: dict[str, Any]):
        if login_value := values.get('login'):
            for field_name in getattr(cls.__config__, 'auth_fields'):
                try:
                    value = cls.__fields__[field_name].type_.validate(login_value)
                    values[field_name] = value
                    break
                except ValueError:
                    pass
        else:
            if not any(x in values for x in getattr(cls.__config__, 'auth_fields')):
                raise ValueError(f'No valid {",".join(x for x in getattr(cls.__config__, "auth_fields"))} for login')
        return values

    def get_auth_field_and_value(self) -> tuple[str, Any]:
        for f in getattr(self.__config__, 'auth_fields'):
            if value := getattr(self, f):
                return f, value  # type: ignore
        raise Exception('Это что такое')

    class Config(CamelModel.Config):
        extra = 'allow'
        auth_fields = ()


class LoginPasswordSchema(BaseLoginPasswordSchema):
    username: Optional[str] = Field(max_length=max_len_of(UserModel)('username'))
    email: Optional[EmailStr]

    class Config(BaseLoginPasswordSchema.Config):
        auth_fields = UserModel.AUTH_FIELDS


class UserReadBase(CamelModelORM):
    id: int
    username: Optional[str]
    email: Optional[EmailStr]
    is_active: bool
    created_at: datetime


class UserRead(UserReadBase):
    pass


class UserMeRead(UserReadBase):
    all_permissions: RelatedList[PermissionRead]
    is_superuser: bool


class UserWriteBase(CamelModel):
    username: Optional[Username] = Field(max_length=max_len_of(UserModel)('username'))
    email: Optional[EmailStr]


class UserEdit(UserWriteBase):
    permissions: Optional[list[int]]
    groups: Optional[list[int]]
    is_superuser: Optional[bool]
    is_active: Optional[bool]


class UserMeEdit(UserWriteBase):
    pass


class UserCreate(PasswordsPair, UserWriteBase):
    permissions: list[int] = []
    groups: list[int] = []
    is_superuser: Optional[bool]
    is_active: Optional[bool]


class UserRegistration(PasswordsPair, UserWriteBase):
    pass


class ChangePassword(PasswordsPair):
    old_password: str

    @validator('old_password')
    def new_is_not_old(cls, v: str, values: dict[str, Any]):
        if v == values.get('password'):
            raise ValueError('newPasswordIsEqualToOld')
        return v
