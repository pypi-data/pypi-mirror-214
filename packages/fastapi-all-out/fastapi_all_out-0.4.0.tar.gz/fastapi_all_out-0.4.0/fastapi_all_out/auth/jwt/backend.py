from warnings import warn
from typing import Callable, Coroutine, Any, cast, Self

from fastapi import APIRouter, Request, BackgroundTasks, Response, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi_all_out.lazy_objects import get_global_objects, get_schema
from fastapi_all_out.routers.exceptions import ItemNotFound
from fastapi_all_out.schemas import LoginPasswordSchema, UserMeRead
from ..base import AuthBackend, BaseUser, SimpleUser, UnauthenticatedUser
from .config import JWTAuthConfig
from .schemas import JWTTokenUser
from .strategy import JWTAuthStrategy


global_objects = get_global_objects()

LoginPasswordSchema = get_schema(LoginPasswordSchema)
UserMeRead = get_schema(UserMeRead)
JWTTokenUser = get_schema(JWTTokenUser)
UserModel = global_objects.USER_MODEL
UserRepository = global_objects.USER_REPOSITORY
UserService = global_objects.USER_SERVICE
Codes = global_objects.CODES


class JWTOAuth2PasswordBearerBackend(AuthBackend):

    strategy: JWTAuthStrategy
    oauth: OAuth2PasswordBearer
    _authenticate: Callable[[Request, str], Coroutine[Any, Any, None]]
    _auth_required: Callable[[Request], Coroutine[Any, Any, None]]
    _load_user: Callable[[Request, BackgroundTasks, Response], Coroutine[Any, Any, None]]
    _load_user_optionally: Callable[[Request, BackgroundTasks, Response], Coroutine[Any, Any, None]]

    def __init__(self, strategy: JWTAuthStrategy, oauth: OAuth2PasswordBearer):
        assert isinstance(strategy, JWTAuthStrategy)
        super().__init__(strategy=strategy)
        self.oauth = oauth

    @classmethod
    def from_config(cls, strategy: JWTAuthStrategy, config: JWTAuthConfig) -> Self:
        return cls(
            strategy=strategy,
            oauth=config.get_oauth2_password_bearer()
        )

    def authenticate_dependency(self) -> Callable[[Request, str], Coroutine[Any, Any, None]]:
        if not hasattr(self, '_authenticate'):
            authenticate_handler = self.strategy.authenticate

            async def authenticate(request: Request, token: str = Depends(self.oauth)) -> None:
                token_data = await authenticate_handler(token)
                if token_data is None:
                    request.scope['auth'] = None
                    request.scope['user'] = UnauthenticatedUser()
                else:
                    user = token_data.user
                    request.scope['auth'] = token_data
                    request.scope['user'] = SimpleUser(
                        pk=user.get_pk(), username=user.username, **user.dict(exclude={'username'})
                    )

            self._authenticate = authenticate

        return self._authenticate

    def auth_required_dependency(self) -> Callable[[Request], Coroutine[Any, Any, None]]:
        if not hasattr(self, '_auth_required'):
            async def auth_required(request: Request) -> None:
                user = cast(SimpleUser | UnauthenticatedUser, request.user)
                if not user.is_authenticated:
                    raise Codes.not_authenticated.err()

            self._auth_required = auth_required
        return self._auth_required

    def load_user_dependency(self) -> Callable[[Request, BackgroundTasks, Response], Coroutine[Any, Any, None]]:
        if not hasattr(self, '_load_user'):
            async def load_user(
                    request: Request,
                    background_tasks: BackgroundTasks,
                    response: Response,
                    _=Depends(self.auth_required_dependency())
            ) -> None:
                user = cast(SimpleUser, request.user)
                if user.is_simple:
                    try:
                        request.scope['user'] = await UserRepository(
                            request=request, background_tasks=background_tasks, response=response
                        ).get_one(user.pk)
                    except ItemNotFound:
                        raise Codes.not_authenticated.err()
                else:
                    warn('What matters? User must be simple there')

            self._load_user = load_user
        return self._load_user

    def load_user_optionally_dependency(self) -> Callable[[Request], Coroutine[Any, Any, None]]:
        if not hasattr(self, '_load_user_optionally'):
            async def load_user_optionally(
                    request: Request,
                    background_tasks: BackgroundTasks,
                    response: Response,
            ):
                user = cast(SimpleUser | UnauthenticatedUser, request.user)
                if not user.is_authenticated:
                    return
                if user.is_simple:
                    try:
                        request.scope['user'] = await UserRepository(
                            request=request, background_tasks=background_tasks, response=response
                        ).get_one(user.pk)
                    except ItemNotFound:
                        return
                else:
                    warn('What matters? User must be simple there')

            self._load_user_optionally = load_user_optionally
        return self._load_user_optionally

    def with_permissions_dependency(
            self,
            *permissions: tuple[str, str],
    ) -> Callable[[Request, BackgroundTasks, Response], Coroutine[Any, Any, None]]:
        async def with_permissions(
                request: Request,
                _=Depends(self.load_user_dependency())
        ) -> None:
            user = cast(BaseUser, request.user)
            if not (user.is_superuser or user.has_permissions(*permissions)):
                raise Codes.permission_denied.err()

        return with_permissions

    def create_router(self, add_refresh_route: bool = True, **kwargs) -> APIRouter:
        router = super().create_router(**kwargs)
        if add_refresh_route:
            self.add_refresh_route(router)
        return router

    @classmethod
    def login_responses(cls):
        return Codes.responses(Codes.not_authenticated)

    def add_login_route(self, router: APIRouter) -> None:
        @router.post(
            '/login', response_model=self.strategy.authorize_response_model,
            responses=self.login_responses()
        )
        async def login(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                form: OAuth2PasswordRequestForm = Depends(),
        ):
            login_password = LoginPasswordSchema(login=form.username, password=form.password)
            field, value = login_password.get_auth_field_and_value()
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks, response=response)\
                    .get_one(value, field_name=field)
            except ItemNotFound:
                raise Codes.not_authenticated.err()

            user_service = UserService(user)
            if not user_service.verify_password(password=login_password.password):
                raise Codes.not_authenticated.err()

            if not user_service.can_login():
                await user_service.if_cant_login(request=request, background_tasks=background_tasks, response=response)
                raise Codes.not_authenticated.err()
            return self.authorize(user)

    def add_logout_route(self, router: APIRouter) -> None:
        pass

    @classmethod
    def refresh_responses(cls):
        return Codes.responses(Codes.not_authenticated)

    def add_refresh_route(self, router: APIRouter) -> None:
        @router.post(
            '/refresh', response_model=self.strategy.authorize_response_model,
            responses=self.refresh_responses()
        )
        async def refresh(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                token: str = Body(..., alias='refreshToken')
        ):
            token = self.strategy.get_refresh_token(token)
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks, response=response)\
                    .get_one(token.user.id)
            except ItemNotFound:
                raise Codes.not_authenticated.err()
            if UserService(user).token_expired(token.iat):
                raise Codes.not_authenticated.err()
            return self.authorize(user)
