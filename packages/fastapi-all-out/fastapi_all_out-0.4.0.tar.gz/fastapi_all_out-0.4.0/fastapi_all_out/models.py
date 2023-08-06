from typing import Any

from fastapi_all_out.enums import Databases
from fastapi_all_out.lazy_objects import get_global_objects


match get_global_objects().auth_db:
    case Databases.tortoise:
        from fastapi_all_out.contrib.tortoise.models import \
            BaseModel, default_of, max_len_of, \
            Permission, PermissionGroup
    case _:
        BaseModel = None
        default_of = None
        max_len_of = None
        Permission = None
        PermissionGroup = None


__all__ = [
    BaseModel, default_of, max_len_of,
    Permission, PermissionGroup
]
