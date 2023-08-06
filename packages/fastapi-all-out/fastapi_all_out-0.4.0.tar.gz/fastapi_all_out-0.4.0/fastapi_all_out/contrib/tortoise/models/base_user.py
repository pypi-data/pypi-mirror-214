from typing import Literal, Optional
from datetime import datetime
from uuid import UUID, uuid4

from tortoise import fields

from . import BaseModel, PermissionMixin


USER_GET_BY_FIELDS = Literal['id', 'email', 'username', 'phone']


class BaseUser(BaseModel):
    id: int = fields.BigIntField(pk=True)
    uuid: UUID = fields.UUIDField(default=uuid4, unique=True)
    username: Optional[str] = fields.CharField(max_length=40, unique=True, null=True)
    email: Optional[str] = fields.CharField(max_length=256, unique=True, null=True)

    password_hash: str = fields.CharField(max_length=200)
    password_change_dt: datetime = fields.DatetimeField()
    password_salt: str = fields.CharField(max_length=50)

    is_superuser: bool = fields.BooleanField(default=False)
    is_active: bool = fields.BooleanField(default=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    AUTH_FIELDS = ('email', 'username')
    IEXACT_FIELDS = ('email', 'username')
    EMAIL_FIELD = 'email'
    EXTRA_PERMISSIONS = ('change_password',)

    class Meta:
        abstract = True

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def is_simple(self) -> bool:
        return False


class UserWithPermissions(BaseUser, PermissionMixin):
    class Meta:
        abstract = True
