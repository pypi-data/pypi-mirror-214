import argparse
import asyncio
from typing import Any
from inspect import iscoroutinefunction
from getpass import getpass

from pydantic.fields import ModelField

from fastapi_all_out.lazy_objects import get_settings
from fastapi_all_out.pydantic import snake_case


class CommandMC(type):
    def __new__(cls, name, bases, attrs: dict, **kwargs):
        command_name = attrs.get('name', name)
        attrs['name'] = snake_case(command_name)
        return super().__new__(cls, name, bases, attrs)


class Command(metaclass=CommandMC):
    name: str
    parser: argparse.ArgumentParser
    help_text: str = 'Write command help text'
    need_db_connection: bool = True

    def __init__(self):
        self.parser = argparse.ArgumentParser(usage=self.help_text)

    def add_arguments(self):
        pass

    async def run(self):
        self.add_arguments()
        databases = get_settings().get_db_config()
        if self.need_db_connection:
            await databases.connect_all()
        if iscoroutinefunction(self.handle):
            await self.handle(**self.parser.parse_args().__dict__)
        else:
            self.handle(**self.parser.parse_args().__dict__)
        if self.need_db_connection:
            await databases.close_all()

    def handle(self, **kwargs):
        raise NotImplementedError('Хоть что-то напиши')

    @classmethod
    def get_valid(cls, field: ModelField, value: str = None, no_input: bool = False) -> Any:
        title = field.alias
        label = title + ': '
        if not no_input:
            value = getpass(label) if 'password' in title.lower() else input(label)
            if field.allow_none and value == '':
                value = None
        try:
            for validator in getattr(field.type_, '__get_validators__', lambda: ())():
                try:
                    value = validator(value)
                except ValueError:
                    raise
                except:
                    continue
            return value
        except ValueError as e:
            print(label, e)
            if no_input:
                raise
            else:
                return cls.get_valid(field)


def list_commands():
    return tuple(map(lambda x: x.name, Command.__subclasses__()))


def run_command(name: str):
    commands = list(filter(lambda x: x.name == name, Command.__subclasses__()))
    match len(commands):
        case 1:
            asyncio.run(commands[0]().run())
        case 0:
            print('нет такой команды :(')
        case _:
            print('Таких команд несколько')
