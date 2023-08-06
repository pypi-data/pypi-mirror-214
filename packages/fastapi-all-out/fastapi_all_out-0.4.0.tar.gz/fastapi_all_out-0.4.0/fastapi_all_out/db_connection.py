from inspect import iscoroutinefunction

from pydantic import BaseModel


class EmptyDatabasesConfig(BaseModel):

    async def connect_all(self):
        for db_name in self.__fields__:
            func = getattr(self, db_name).connect
            if iscoroutinefunction(func):
                await func()
            else:
                func()

    async def close_all(self):
        for db_name in self.__fields__:
            func = getattr(self, db_name).close
            if iscoroutinefunction(func):
                await func()
            else:
                func()

