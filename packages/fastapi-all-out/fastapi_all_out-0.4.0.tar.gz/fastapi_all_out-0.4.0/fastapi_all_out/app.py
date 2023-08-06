from fastapi import FastAPI, APIRouter, Depends

from fastapi_all_out.responses import \
    default_exception_handlers, \
    change_openapi_validation_error_schema
from fastapi_all_out.lazy_objects import get_settings, get_global_objects


class ExFastAPI(FastAPI):
    router: APIRouter

    def __init__(
            self,
            *,
            add_auth_dependency: bool = True,
            **kwargs
    ) -> None:
        kwargs.setdefault('swagger_ui_parameters', {"operationsSorter": "method", "docExpansion": "none"})
        exception_handlers = kwargs.get('exception_handlers', {})
        kwargs['exception_handlers'] = {**default_exception_handlers, **exception_handlers}
        if add_auth_dependency:
            dependencies = kwargs.get('dependencies', [])
            auth_backend = get_global_objects().AUTH_BACKEND
            kwargs['dependencies'] = [Depends(auth_backend.authenticate_dependency()), *dependencies]
        super().__init__(**kwargs)

        # db connections
        databases = get_settings().get_db_config()
        self.router.on_startup.append(databases.connect_all)
        self.router.on_shutdown.append(databases.close_all)

        async def default_on_start():
            try:
                change_openapi_validation_error_schema(self)
            except KeyError:
                pass

        self.router.on_startup.append(default_on_start)
