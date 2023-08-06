from fastapi import APIRouter

from fastapi_all_out.routers import CRUDRouter
from fastapi_all_out.lazy_objects import get_schema, get_global_objects
from fastapi_all_out.models import Permission, PermissionGroup
from fastapi_all_out.schemas import PermissionRead, PermissionGroupRead, PermissionGroupCreate, PermissionGroupEdit


Repository = get_global_objects().REPOSITORY


def get_roles_router(prefix: str = '/roles', **kwargs) -> APIRouter:
    router = APIRouter(prefix=prefix, **kwargs)

    router.include_router(CRUDRouter(
        repo=type('PermissionRepository', (Repository, ), {'model': Permission}),  # type: ignore
        read_schema=get_schema(PermissionRead),
        read_only=True,
    ))

    router.include_router(CRUDRouter(
        repo=type('PermissionGroupRepository', (Repository, ), {'model': PermissionGroup}),  # type: ignore
        read_schema=get_schema(PermissionGroupRead),
        edit_schema=get_schema(PermissionGroupEdit),
        create_schema=get_schema(PermissionGroupCreate),
    ))

    return router
