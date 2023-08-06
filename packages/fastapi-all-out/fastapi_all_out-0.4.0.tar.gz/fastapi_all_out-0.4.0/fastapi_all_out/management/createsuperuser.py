import json
from typing import Type

from fastapi_all_out.schemas import UserCreate
from fastapi_all_out.pydantic import CamelModel
from fastapi_all_out.lazy_objects import get_global_objects, get_schema
from fastapi_all_out.routers.exceptions import ObjectErrors
from fastapi_all_out.management import Command


UserCreate = get_schema(UserCreate)
UserRepository = get_global_objects().USER_REPOSITORY


def exclude_fields(schema: Type[CamelModel], fields: tuple[str, ...]):
    return {k: v for k, v in schema.__fields__.items() if k not in fields}


def include_fields(schema: Type[CamelModel], fields: tuple[str, ...]):
    return {k: v for k, v in schema.__fields__.items() if k in fields}


class CreateSuperuser(Command):
    name = 'createsuperuser'
    fields = include_fields(UserCreate, UserRepository.get_create_superuser_fields())

    async def handle(self, **kwargs):
        no_input = kwargs['no_input']
        data = {k: v for k, v in kwargs.items() if k in self.fields and v is not None}
        if no_input and 'password' in data and 're_password' not in data:
            data['re_password'] = data['password']
        for field_name, field in self.fields.items():
            data[field_name] = self.get_valid(field, value=data.get(field_name), no_input=no_input)

        try:
            await UserRepository().create_superuser(UserCreate(**data).dict(exclude_unset=True))
        except ObjectErrors as e:
            print(json.dumps(e.to_error(), indent=4, ensure_ascii=False))

    def add_arguments(self):
        self.parser.add_argument('--no-input', action='store_true')
        for field in self.fields:
            self.parser.add_argument('--' + field)



