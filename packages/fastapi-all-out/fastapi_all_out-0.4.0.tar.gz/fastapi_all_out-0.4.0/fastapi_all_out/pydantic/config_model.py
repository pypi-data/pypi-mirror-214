from pydantic import BaseModel, BaseConfig


class ConfigModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return string.lower()
