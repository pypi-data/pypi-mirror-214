from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel


def snake_case(string: str) -> str:
    res = ''
    for c in string:
        if c.isupper():
            res += '_' + c.lower()
        else:
            res += c
    if res.startswith('_'):
        res = res[1:]
    return res


def lower_camel(string: str) -> str:
    fragments = []
    for frag in string.split('__'):
        temp = frag.split('_')
        fragments.append(temp[0] + ''.join(elem.title() for elem in temp[1:]))
    return '__'.join(fragments)


try:
    import orjson

    def dumps(v, *, default, **kwargs):
        return orjson.dumps(v, default=default, **kwargs).decode()

    loads = orjson.loads
except ImportError:
    import json
    dumps = json.dumps
    loads = json.loads


class CamelConfig:
    allow_population_by_field_name = True
    anystr_strip_whitespace = True
    alias_generator = lower_camel

    json_loads = loads
    json_dumps = dumps
    json_encoders = {
        UUID: lambda v: str(v),
        Enum: lambda v: v.value,
        set: lambda v: list(v),
    }


class CamelModel(BaseModel):
    Config = CamelConfig


class CamelModelORM(CamelModel):
    class Config(CamelConfig):
        orm_mode = True


class CamelGeneric(GenericModel):
    Config = CamelConfig
