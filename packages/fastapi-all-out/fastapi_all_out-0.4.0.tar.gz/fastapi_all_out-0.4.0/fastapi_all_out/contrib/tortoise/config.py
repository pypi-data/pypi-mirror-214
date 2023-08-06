from typing import Any, Type, cast

from tortoise import Tortoise, connections
from tortoise.log import logger

from .models import BaseModel
from fastapi_all_out.pydantic import ConfigModel


class TortoiseOrmConfig(ConfigModel):
    DB_NAME: str
    DB_USER: str = 'postgres'
    DB_PWD: str = 'postgres'
    DB_HOST: str = '127.0.0.1'
    DB_PORT: str = '5432'

    apps: tuple[str, ...] = ('models', )
    engine: str = 'tortoise.backends.asyncpg'
    check_permissions: bool = True

    def get_config(self) -> dict[str, Any]:
        return {
            'connections': {
                'default': {
                    "engine": self.engine,
                    'credentials': {
                        'host': self.DB_HOST,
                        'port': self.DB_PORT,
                        'user': self.DB_USER,
                        'password': self.DB_PWD,
                        'database': self.DB_NAME,
                    },
                }
            },
            'apps': {
                'models': {
                    'models': [
                        'aerich.models',
                        *self.apps,
                    ]
                }
            },
        }

    async def connect(self):
        await Tortoise.init(config=self.get_config())
        logger.info(f'Tortoise-ORM started, {connections._get_storage()}, {Tortoise.apps}')
        if self.check_permissions:
            await check_permissions()

    @classmethod
    async def close(cls):
        await connections.close_all()
        logger.info("Tortoise-ORM shutdown")


async def check_permissions():
    from aerich.models import Aerich
    from .models import ContentType, Permission
    # The requirement is to use only the fastapi_all_our.contrib.tortoise.models.BaseModel, not tortoise.Model
    all_models = cast(list[Type[BaseModel]], list(Tortoise.apps.get('models').values()))
    if ContentType not in all_models:
        return
    old_names = [ct.name async for ct in ContentType.all()]
    new_names = []
    for model in all_models:
        if model not in (Aerich, ContentType):
            model_name = model.__name__
            if model_name in old_names:
                old_names.remove(model_name)
            else:
                new_names.append(model_name)
    if old_names:
        await ContentType.filter(name__in=old_names).delete()
    if new_names:
        await ContentType.bulk_create([ContentType(name=n) for n in new_names])
    content_types = await ContentType.all()
    permissions = await Permission.all()

    create_perms: list[Permission] = []
    delete_perm_ids: list[int] = []
    for ct in content_types:
        ContentType.instances_by_id[ct.id] = ct
        ContentType.instances_by_name[ct.name] = ct

        model: Type[BaseModel] = Tortoise.apps['models'][ct.name]  # type: ignore
        need_perm_names: list[str] = [*model.BASE_PERMISSIONS, *model.EXTRA_PERMISSIONS]
        for perm in filter(lambda p: p.content_type_id == ct.id, permissions):
            if perm.name in need_perm_names:
                need_perm_names.remove(perm.name)
            else:
                delete_perm_ids.append(perm.id)
        if need_perm_names:
            create_perms.extend(Permission(content_type=ct, name=perm_name) for perm_name in need_perm_names)
    if create_perms:
        await Permission.bulk_create(create_perms)
    if delete_perm_ids:
        await Permission.filter(id__in=delete_perm_ids)
