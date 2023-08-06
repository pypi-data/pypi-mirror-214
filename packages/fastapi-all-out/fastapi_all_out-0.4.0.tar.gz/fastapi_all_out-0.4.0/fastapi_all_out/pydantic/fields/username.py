import re
from typing import Any

from pydantic.validators import strict_str_validator


class Username(str):

    min_len = 2
    max_len = 30
    pattern = re.compile(r'^(?=.*[a-z])[a-z0-9+._-]+$')

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type='string', format='username', example='sasha_molodez')

    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        if cls.pattern.match(v) is None:
            # Lowercase letters (at least one) and symbols +._- (optional)
            raise ValueError('invalidUsername')
        if getattr(cls, 'max_len', None) and len(v) > cls.max_len:
            raise ValueError('longUsername')
        if getattr(cls, 'min_len', None) and len(v) < cls.min_len:
            raise ValueError('shortUsername')
        return cls(v)
