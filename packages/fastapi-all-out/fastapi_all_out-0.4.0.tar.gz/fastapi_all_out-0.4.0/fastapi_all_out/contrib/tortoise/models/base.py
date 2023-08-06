from collections.abc import Callable
from typing import Any, Type

from tortoise import Model as DefaultModel


class BaseModel(DefaultModel):
    IEXACT_FIELDS: set[str] = ()
    BASE_PERMISSIONS: tuple[str, ...] = ('get', 'create', 'edit', 'delete')
    EXTRA_PERMISSIONS: tuple[str, ...] = ()

    class Meta:
        abstract = True


def get_field_param(model: Type[BaseModel], field_name: str, field_param: str):
    return getattr(model._meta.fields_map[field_name], field_param)


def max_len_of(model: Type[BaseModel]) -> Callable[[str], int]:
    return lambda field_name: get_field_param(model, field_name, 'max_length')


def default_of(model: Type[BaseModel]) -> Callable[[str], Any]:
    return lambda field_name: get_field_param(model, field_name, 'default')
