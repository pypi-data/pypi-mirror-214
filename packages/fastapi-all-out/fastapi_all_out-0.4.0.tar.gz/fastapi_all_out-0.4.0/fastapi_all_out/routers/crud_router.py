from collections.abc import Sequence
from enum import Enum
from typing import Callable, Any, Generic, TypeVar, Optional, Type, Literal, TypedDict, Final, Union, List, Dict, Set

from fastapi import Response, Request, APIRouter, Body, Path, Query, Depends, BackgroundTasks
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.encoders import SetIntStr, DictIntStrAny
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id
from pydantic.error_wrappers import ErrorWrapper
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute

from fastapi_all_out.code_responses import BaseCodes
from fastapi_all_out.pydantic import CommaSeparatedOf, lower_camel, CamelModel
from fastapi_all_out.lazy_objects import get_global_objects
from fastapi_all_out.responses import BgHTTPException
from fastapi_all_out.routers import BaseRepository
from .exceptions import ItemNotFound, ObjectErrors
from .filters import BaseFilter
from .utils import \
    pagination_factory, PAGINATION,\
    filters_factory, FILTERS, \
    sort_factory, SORT


CHECK_PERMS: Final[str] = 'check_perms'
LOAD_USER: Final[str] = 'load_user'
AUTH_REQUIRED: Final[str] = 'auth_required'
LOAD_USER_OPTIONALLY: Final[str] = 'load_user_optionally'
ACCESS_ALL: Final[str] = 'access_all'
ACCESS = Literal['check_perms', 'load_user', 'auth_required', 'load_user_optionally', 'access_all']

REPO = TypeVar('REPO', bound=BaseRepository)
DEPENDENCIES = Optional[Sequence[Depends]]
ROUTE_KWARGS = TypedDict('ROUTE_KWARGS', total=False, fields={
    'dependencies': DEPENDENCIES,
    'access': ACCESS
})
ROUTES_KWARGS = dict[str, ROUTE_KWARGS]
global_objects = get_global_objects()
Codes = global_objects.CODES
auth_backend = global_objects.AUTH_BACKEND


class CRUDRouter(Generic[REPO], APIRouter):
    repo: Type[REPO]
    max_items_get_many_routes: Optional[int]
    max_items_delete_many_routes: Optional[int]
    filters: list[Type[BaseFilter]]
    available_sort: set[str]
    max_page_size: int | None
    tree_enabled: bool

    read_schema: Optional[Type[CamelModel]]
    read_many_schema: Optional[Type[CamelModel]]
    read_list_item_schema: Optional[Type[CamelModel]]
    create_schema: Optional[Type[CamelModel]]
    edit_schema: Optional[Type[CamelModel]]

    def __init__(
            self,
            repo: Type[REPO],
            *,
            read_schema: Optional[Type[CamelModel]] = None,
            read_many_schema: Optional[Type[CamelModel]] = None,
            read_list_item_schema: Optional[Type[CamelModel]] = None,
            create_schema: Optional[Type[CamelModel]] = None,
            edit_schema: Optional[Type[CamelModel]] = None,
            max_items_get_many: int = 100,
            max_items_delete_many: int = 100,
            prefix: str = None,
            tags: Optional[list[str | Enum]] = None,
            filters: list[Type[BaseFilter]] = None,
            available_sort: set[str] = None,
            max_page_size: int | None = 100,
            routes_kwargs: ROUTES_KWARGS = None,
            tree_enabled: bool = False,
            read_only: bool = False,
            routes_only: set[str] = None,
            complete_auto_routes: bool = True,
            **kwargs,
    ) -> None:
        """
            :param max_items_get_many         отпределяет маскимальное количество записей, которые достаются по id
            :param max_items_delete_many      отпределяет маскимальное количество записей, которые удаляются по id
            :param prefix                     префикс из APIRouter
            :param tags                       tags из APIRouter
            :param filters                    фильтры для get_all
            :param available_sort             поля для сортировки для get_all
            :param auto_routes_dependencies   инъекции которые применяются для всех роутов, сгенерированных
                                              автоматически, если нужно для всех, не только автоматически
                                              сгенерированных, то нужно использовать dependencies
            :param routes_kwargs              словарь вида {route_name: add_api_route kwargs},
                                              значение может быть равно False, если этот роут не нужен ({create: False})
            :param add_tree_routes            добавляет методы для деревьев
            :param read_only                  создаёт только get методы
            :param routes_only                set из роутов, которые нужно создать
            :param complete_auto_routes       если нужно создать какие-то роуты, без Path параметров, которые просто так
                                              перекрываются
            :param kwargs                     всё что передаётся в APIRouter
        """

        self.repo = repo
        prefix = prefix.strip('/') if prefix else self.repo.model.__name__.lower() + 's'
        tags = tags or [prefix]
        prefix = '/' + prefix
        super().__init__(prefix=prefix, tags=tags, **kwargs)

        self.read_schema = read_schema
        self.read_many_schema = read_many_schema or self.read_schema
        self.read_list_item_schema = read_list_item_schema or self.read_many_schema
        self.create_schema = create_schema
        self.edit_schema = edit_schema

        self.max_items_get_many_routes = max_items_get_many
        self.max_items_delete_many_routes = max_items_delete_many
        self.read_only = read_only
        self.tree_enabled = tree_enabled

        self.routes_kwargs = routes_kwargs or {}

        if routes_only:
            routes_names = routes_only
        else:
            routes_names = []
            for rn in self.default_route_names():
                if self.routes_kwargs.get(rn) is not False:
                    routes_names.append(rn)
        self.routes_names = tuple(routes_names)

        if filters is None:
            filters = []
        self.filters = filters
        self.available_sort = available_sort or self.repo.get_default_sort_fields()
        self.max_page_size = max_page_size

        if complete_auto_routes:
            self.complete_auto_routes()

    def complete_auto_routes(self) -> None:
        for route_name in self.routes_names:
            getattr(self, f'_register_{route_name}')()

    def get_dependencies(
            self,
            route_name: str,
            access: str = ACCESS_ALL,
            permissions: Sequence[str] = None,
    ) -> DEPENDENCIES:
        """
        :param route_name: name of route (get_all, get_many, ..., create, delete_one, ...)
        :param access: type of access.
        :param permissions: names of permissions to check if access == 'check_perms.
        :return: DEPENDENCIES
        """
        route_kwargs: ROUTE_KWARGS = {**self.routes_kwargs.get('_all', {}), **self.routes_kwargs.get(route_name, {})}
        dependencies = route_kwargs.get('dependencies', ())
        access = route_kwargs.get('access', access)
        assert access in (CHECK_PERMS, LOAD_USER, LOAD_USER_OPTIONALLY, AUTH_REQUIRED, ACCESS_ALL)

        if access == CHECK_PERMS:
            if permissions:
                check_perms_dep = Depends(self.repo.with_model_permissions(*permissions))
            elif route_name in self.GET_names():
                check_perms_dep = Depends(self.repo.with_model_permissions('get'))
            elif route_name in self.CREATE_names():
                check_perms_dep = Depends(self.repo.with_model_permissions('create'))
            elif route_name in self.EDIT_names():
                check_perms_dep = Depends(self.repo.with_model_permissions('edit'))
            elif route_name in self.DELETE_names():
                check_perms_dep = Depends(self.repo.with_model_permissions('delete'))
            else:
                raise Exception('If access is check_perms, permissions must be passed '
                                'or route_name must be in GET_names, CREATE_names, EDIT_names or DELETE_names')
            return *dependencies, check_perms_dep
        elif access == LOAD_USER:
            return *dependencies, Depends(auth_backend.load_user_dependency())
        elif access == AUTH_REQUIRED:
            return *dependencies, Depends(auth_backend.auth_required_dependency())
        elif access == LOAD_USER_OPTIONALLY:
            return *dependencies, Depends(auth_backend.load_user_optionally_dependency())
        return *dependencies,

    def get_read_schema(self) -> Type[CamelModel]:
        return self.read_schema

    def get_read_many_schema(self) -> Type[CamelModel]:
        return self.read_many_schema

    def get_read_list_item_schema(self) -> Type[CamelModel]:
        return self.read_list_item_schema

    def get_create_schema(self) -> Type[CamelModel]:
        return self.create_schema

    def get_edit_schema(self) -> Type[CamelModel]:
        return self.edit_schema

    def register_api_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            access: str = ACCESS_ALL,
            permissions: Sequence[str] = None,
            dependencies: DEPENDENCIES = None,

            response_model: Any = Default(None),
            status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            deprecated: Optional[bool] = None,
            methods: Optional[Union[Set[str], List[str]]] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
            name: Optional[str] = None,
            route_class_override: Optional[Type[APIRoute]] = None,
            callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Union[
                Callable[[APIRoute], str], DefaultPlaceholder
            ] = Default(generate_unique_id),
    ) -> None:
        name = name or endpoint.__name__
        assert name in self.routes_names
        self.add_api_route(
            path,
            endpoint,
            dependencies=dependencies or self.get_dependencies(name, access, permissions=permissions),
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            route_class_override=route_class_override,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    # get_all GET /all
    def _get_all_route(self) -> Callable[..., Any]:
        list_item_schema = self.get_read_list_item_schema()

        async def get_all(
                background_tasks: BackgroundTasks,
                request: Request,
                response: Response,
                pagination: PAGINATION = pagination_factory(self.max_page_size),
                sort: SORT = Depends(sort_factory(self.available_sort)),
                filters: FILTERS = Depends(filters_factory(self.filters))
        ):
            raise_if_error_in_filters(filters)
            skip, limit = pagination
            repository = self.repo(request=request, background_tasks=background_tasks, response=response)
            result, total = await repository.get_all(
                skip=skip,
                limit=limit,
                sort=sort,
                filters=filters,
            )
            response.headers.append('X-Total-Count', str(total))
            return [list_item_schema.from_orm(r) for r in result]

        return get_all

    def _register_get_all(self) -> None:
        self.register_api_route(
            path='/all',
            endpoint=self._get_all_route(),
            methods=["GET"],
            response_model=list[self.get_read_list_item_schema()],
            summary='Get all ' + self.repo.model.__name__,
            status_code=200,
            openapi_extra={'parameters': [f.query_openapi_desc() for f in self.filters]},
            access=CHECK_PERMS,
        )

    # get_many GET /many
    def _get_many_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        max_items = self.max_items_get_many_routes
        read_many_schema = self.get_read_many_schema()

        async def get_many(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                item_ids: CommaSeparatedOf(pk_field_type, max_items=max_items, in_query=True) = Query(..., alias='ids')
        ):
            repository = self.repo(request=request, background_tasks=background_tasks, response=response)
            results = await repository.get_many(item_ids)
            return [read_many_schema.from_orm(r) for r in results]

        return get_many

    def _register_get_many(self) -> None:
        self.register_api_route(
            path='/many',
            endpoint=self._get_many_route(),
            methods=["GET"],
            response_model=list[self.get_read_many_schema()],
            summary='Get many ' + self.repo.model.__name__,
            status_code=200,
            access=CHECK_PERMS
        )

    # get_one GET /one/{item_id}
    def _get_one_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        read_schema = self.get_read_schema()

        async def get_one(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                item_id: pk_field_type = Path(...),
        ):
            try:
                repository = self.repo(request=request, background_tasks=background_tasks, response=response)
                item = await repository.get_one(item_id)
            except ItemNotFound:
                raise self.not_found_error()
            return read_schema.from_orm(item)

        return get_one

    def _register_get_one(self) -> None:
        self.register_api_route(
            path='/one/{item_id}',
            endpoint=self._get_one_route(),
            methods=["GET"],
            response_model=self.get_read_schema(),
            summary='Get one ' + self.repo.model.__name__,
            status_code=200,
            access=CHECK_PERMS,
            responses=Codes.responses(self.not_found_error_instance()),
        )

    # get_tree_node GET /tree
    def _get_tree_node_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        get_list_item_schema = self.get_read_list_item_schema()

        async def get_tree_node(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                node_id: Optional[pk_field_type] = Query(None, alias=lower_camel(self.repo.node_key))
        ):
            repository = self.repo(request=request, background_tasks=background_tasks, response=response)
            return [get_list_item_schema.from_orm(item) for item in await repository.get_tree_node(node_id)]

        return get_tree_node

    def _register_get_tree_node(self) -> None:
        self.register_api_route(
            path='/tree',
            endpoint=self._get_tree_node_route(),
            methods=["GET"],
            response_model=list[self.get_read_list_item_schema()],
            summary='Get tree node ' + self.repo.model.__name__,
            status_code=200,
            access=CHECK_PERMS
        )

    # create POST /create
    def _create_route(self) -> Callable[..., Any]:
        create_schema = self.get_create_schema()
        read_schema = self.get_read_schema()

        async def create(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                data: create_schema = Body(...)
        ):
            try:
                instance = await self.repo(request=request, background_tasks=background_tasks, response=response)\
                    .create(data.dict(exclude_unset=True))
            except ObjectErrors as e:
                raise self.field_errors(e)
            return read_schema.from_orm(instance)

        return create

    def _register_create(self) -> None:
        self.register_api_route(
            path='/create',
            endpoint=self._create_route(),
            methods=["POST"],
            response_model=self.get_read_schema(),
            summary='Create ' + self.repo.model.__name__,
            status_code=201,
            access=CHECK_PERMS,
            responses=Codes.responses(self.field_errors_response_example()),
        )

    # edit PATCH /{item_id}
    def _edit_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        read_schema = self.get_read_schema()
        edit_schema = self.get_edit_schema()

        async def edit(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                item_id: pk_field_type = Path(...),
                data: edit_schema = Body(...)
        ):
            repository = self.repo(request=request, background_tasks=background_tasks, response=response)
            try:
                instance = await repository.get_one(item_id)
            except ItemNotFound:
                raise self.not_found_error()
            try:
                instance = await repository.edit(instance, data.dict(exclude_unset=True))
            except ObjectErrors as e:
                raise self.field_errors(e)
            return read_schema.from_orm(instance)

        return edit

    def _register_edit(self) -> None:
        self.register_api_route(
            path='/{item_id}',
            endpoint=self._edit_route(),
            methods=["PATCH"],
            response_model=self.get_read_schema(),
            summary='Edit ' + self.repo.model.__name__,
            status_code=200,
            access=CHECK_PERMS,
            responses=Codes.responses(
                self.not_found_error_instance(),
                self.field_errors_response_example()
            )
        )

    # delete_many DELETE /many
    def _delete_many_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type
        max_items = self.max_items_get_many_routes

        async def delete_many(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                item_ids: CommaSeparatedOf(pk_field_type, max_items=max_items, in_query=True) = Query(..., alias='ids')
        ):
            repository = self.repo(request=request, background_tasks=background_tasks, response=response)
            deleted_items_count = await repository.delete_many(item_ids)
            return self.ok_response(count=deleted_items_count)

        return delete_many

    def _register_delete_many(self) -> None:
        self.register_api_route(
            path='/many',
            endpoint=self._delete_many_route(),
            methods=["DELETE"],
            summary='Delete many ' + self.repo.model.__name__,
            status_code=200,
            access=CHECK_PERMS,
            responses=Codes.responses((self._ok_response_instance(), {'count': 30}), )
        )

    # delete_one DELETE /{item_id}
    def _delete_one_route(self) -> Callable[..., Any]:
        pk_field_type = self.repo.pk_field_type

        async def delete_one(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                item_id: pk_field_type = Path(...)
        ):
            repository = self.repo(request=request, background_tasks=background_tasks, response=response)
            try:
                instance = await repository.get_one(item_id)
            except ItemNotFound:
                raise self.not_found_error()
            await repository.delete_one(instance=instance)
            return self.ok_response(item=item_id)

        return delete_one

    def _register_delete_one(self) -> None:
        self.register_api_route(
            path='/{item_id}',
            endpoint=self._delete_one_route(),
            methods=["DELETE"],
            summary='Delete one ' + self.repo.model.__name__,
            status_code=200,
            access=CHECK_PERMS,
            responses=Codes.responses((self._ok_response_instance(), {'item': 77}), )
        )

    @classmethod
    def _ok_response_instance(cls) -> BaseCodes:
        return Codes.OK

    def ok_response(self, **kwargs) -> dict[str, Any]:
        if kwargs:
            return self._ok_response_instance().resp_detail(**kwargs)
        return self._ok_response_instance().resp

    @classmethod
    def not_found_error_instance(cls) -> BaseCodes:
        return Codes.not_found

    def not_found_error(self) -> BgHTTPException:
        return self.not_found_error_instance().err()

    @classmethod
    def field_errors_instance(cls) -> BaseCodes:
        return Codes.fields_error

    def field_errors_response_example(self, example: dict[str, Any] = None) -> tuple[BaseCodes, dict[str, str]]:
        return (self.field_errors_instance(), {
            'errors': example or 'Объект, который соответствует заполняемой модели, но вместо значений - ошибки'
        })

    def field_errors(self, object_errors: ObjectErrors) -> BgHTTPException:
        return self.field_errors_instance().err({'errors': object_errors.to_error()})

    def default_route_names(self) -> tuple[str, ...]:
        if self.read_only:
            return self.GET_names()
        return *self.GET_names(), *self.CREATE_names(), *self.EDIT_names(), *self.DELETE_names(), *self.EXTRA_names()

    def GET_names(self) -> tuple[str, ...]:
        names = 'get_all', 'get_many', 'get_one'
        return (*names, 'get_tree_node') if self.tree_enabled else names

    def CREATE_names(self) -> tuple[str, ...]:
        return 'create',

    def EDIT_names(self) -> tuple[str, ...]:
        return 'edit',

    def DELETE_names(self) -> tuple[str, ...]:
        return 'delete_many', 'delete_one'

    def EXTRA_names(self) -> tuple[str, ...]:
        return ()


def raise_if_error_in_filters(filters: list[BaseFilter]) -> None:
    errors = [ErrorWrapper(f.error, loc=("filters", f.camel_source)) for f in filters if f.error is not None]
    if errors:
        raise RequestValidationError(errors)
