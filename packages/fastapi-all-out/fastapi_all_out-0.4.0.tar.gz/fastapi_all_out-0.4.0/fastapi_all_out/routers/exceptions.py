from typing import Union, Type, Self

from fastapi_all_out.pydantic import lower_camel


class ItemNotFound(Exception):
    pass


class FieldError(Exception):
    key: str

    @classmethod
    def to_error(cls):
        return cls.key


class AnyFieldError(FieldError):
    def __init__(self, key: str, to_camel: bool = True):
        self.key = lower_camel(key) if to_camel else key

    def to_error(self):
        return self.key


NotUnique = AnyFieldError('not_unique')
NotFoundFK = AnyFieldError('notFoundFK', False)
FieldRequired = AnyFieldError('required_field')
OldPasswordIsIncorrect = AnyFieldError('old_password_is_incorrect')


class ListFieldError(FieldError):
    objects_map: dict[int, Union["ObjectErrors", "FieldError"]]

    def __init__(self,  *args):
        super().__init__(*args)
        self.objects_map = {}

    def append(self, index: int, err: Union[Type["FieldError"], "FieldError", "ObjectErrors"]):
        self.objects_map[index] = err

    def to_error(self):
        return {index: error.to_error() for index, error in self.objects_map.items()}

    def __bool__(self):
        return not not self.objects_map


class ObjectErrors(Exception):
    errors: dict[str, Union[Type["FieldError"], "FieldError", "ObjectErrors"]]

    def __init__(self, *args):
        super().__init__(*args)
        self.errors = {}

    def __str__(self):
        return str(self.to_error())

    def to_error(self):
        return {key: error.to_error() for key, error in self.errors.items()}

    def add(self, field: str, error: Union[Type["FieldError"], "FieldError", "ObjectErrors"]) -> Self:
        self.errors[field] = error
        return self

    def merge(self, obj_error: "ObjectErrors") -> Self:
        self.errors.update(obj_error.errors)
        return self

    def __bool__(self):
        return not not self.errors
