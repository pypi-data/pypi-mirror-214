from typing import Callable, Any, Optional, Type, cast
from uuid import uuid4, UUID

from fastapi import Request, BackgroundTasks, Response, Body, Query, Path
from pydantic import EmailStr, PositiveInt

from fastapi_all_out.auth.base import BaseUser
from fastapi_all_out.enums import TempCodeTriggers
from fastapi_all_out.lazy_objects import get_global_objects, get_schema
from fastapi_all_out.pydantic import CamelModel
from fastapi_all_out.routers import CRUDRouter
from fastapi_all_out.routers.crud_router import LOAD_USER, ACCESS_ALL, LOAD_USER_OPTIONALLY, CHECK_PERMS, REPO
from fastapi_all_out.routers.exceptions import ObjectErrors, ItemNotFound, OldPasswordIsIncorrect
from fastapi_all_out.schemas import UserRead, UserMeRead, UserEdit, UserMeEdit, UserCreate, UserRegistration,\
    ChangePassword, PasswordsPair


global_objects = get_global_objects()

auth_backend = global_objects.AUTH_BACKEND
UserRepository = global_objects.USER_REPOSITORY
UserService = global_objects.USER_SERVICE
Codes = global_objects.CODES

UserRead = get_schema(UserRead)
UserMeRead = get_schema(UserMeRead)
UserEdit = get_schema(UserEdit)
UserMeEdit = get_schema(UserMeEdit)
UserCreate = get_schema(UserCreate)
UserRegistration = get_schema(UserRegistration)
ChangePassword = get_schema(ChangePassword)


class UserRouter(CRUDRouter[REPO]):
    read_me_schema: Optional[Type[CamelModel]]
    edit_me_schema: Optional[Type[CamelModel]]
    registration_schema: Optional[Type[CamelModel]]

    def __init__(
            self,
            *,
            read_schema: Optional[Type[CamelModel]] = UserRead,
            read_me_schema: Optional[Type[CamelModel]] = UserMeRead,
            read_many_schema: Optional[Type[CamelModel]] = None,
            read_list_item_schema: Optional[Type[CamelModel]] = None,
            create_schema: Optional[Type[CamelModel]] = UserCreate,
            registration_schema: Optional[Type[CamelModel]] = UserRegistration,
            edit_schema: Optional[Type[CamelModel]] = UserEdit,
            edit_me_schema: Optional[Type[CamelModel]] = UserMeEdit,
            **kwargs,
    ):
        self.read_me_schema = read_me_schema
        self.registration_schema = registration_schema
        self.edit_me_schema = edit_me_schema
        super().__init__(
            UserRepository,
            read_schema=read_schema,
            read_many_schema=read_many_schema,
            read_list_item_schema=read_list_item_schema,
            create_schema=create_schema,
            edit_schema=edit_schema,
            **kwargs
        )

    # get_me GET /me
    def _get_me_route(self) -> Callable[..., Any]:
        async def get_me(request: Request):
            return self.read_me_schema.from_orm(request.user)

        return get_me

    def _register_get_me(self) -> None:
        self.register_api_route(
            path='/me',
            endpoint=self._get_me_route(),
            methods=["GET"],
            response_model=self.read_me_schema,
            summary='Get me',
            status_code=200,
            access=LOAD_USER,
            responses=Codes.responses(*Codes.auth_errors()),
        )

    # edit_me PATCH /me
    def _edit_me_route(self) -> Callable[..., Any]:
        edit_me_schema = self.edit_me_schema

        async def edit_me(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                data: edit_me_schema = Body(...),
        ):
            try:
                instance = await self.repo(request=request, background_tasks=background_tasks, response=response) \
                    .edit(request.user, data.dict(exclude_unset=True))
            except ObjectErrors as e:
                raise self.field_errors(e)
            return self.read_me_schema.from_orm(instance)

        return edit_me

    def _register_edit_me(self) -> None:
        self.register_api_route(
            path='/me',
            endpoint=self._edit_me_route(),
            methods=["PATCH"],
            response_model=self.read_me_schema,
            summary='Edit me',
            status_code=200,
            access=LOAD_USER,
            responses=Codes.responses(*Codes.auth_errors()),
        )

    # registration POST /registration
    def _registration_route(self) -> Callable[..., Any]:
        registration_schema = self.registration_schema

        async def registration(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                data: registration_schema = Body(...)
        ):
            try:
                user = await self.repo(request=request, background_tasks=background_tasks, response=response)\
                    .create(data.dict(exclude_unset=True))
            except ObjectErrors as e:
                raise self.field_errors(e)
            await UserService(user).post_registration(
                request=request, background_tasks=background_tasks, response=response
            )
            return Codes.activation_email.resp_detail(uuid=user.uuid)

        return registration

    def _register_registration(self) -> None:
        self.register_api_route(
            path='/registration',
            endpoint=self._registration_route(),
            methods=["POST"],
            summary='Registration',
            status_code=201,
            access=ACCESS_ALL,
            responses=Codes.responses(
                (Codes.activation_email, {'uuid': uuid4()}),
                self.field_errors_response_example()
            ),
        )

    # activation GET /activation
    def _activation_route(self) -> Callable[..., Any]:
        async def activation(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                uuid: UUID = Query(...),
                code: str = Query(..., min_length=6, max_length=6)
        ):
            user_repo = self.repo(request=request, background_tasks=background_tasks, response=response)
            try:
                user = user_repo.get_one(uuid, field_name='uuid')
            except ItemNotFound:
                raise self.not_found_error()
            user_service = UserService(user)
            if user_service.user.is_active:
                raise Codes.already_active.err()
            temp_code = await user_service.get_temp_code(trigger=TempCodeTriggers.EmailActivation)
            if not temp_code:
                background_tasks.add_task(user_service.send_activation_email)
                raise Codes.activation_email_resend.err(background=background_tasks)
            if temp_code_error := user_service.check_temp_code_error(code, temp_code):
                if temp_code_error == 'expired':
                    background_tasks.add_task(user_service.send_activation_email)
                    raise Codes.activation_email_resend.err(background=background_tasks)
                else:
                    raise Codes.code_incorrect.err()
            await user_repo.edit(user, {'is_active': True})
            await user_service.delete_temp_code(temp_code)
            return auth_backend.authorize(user_service.user)
        return activation

    def _register_activation(self) -> None:
        self.register_api_route(
            path='/activation',
            endpoint=self._activation_route(),
            methods=["GET"],
            response_model=auth_backend.strategy.authorize_response_model,
            summary='User activation',
            status_code=200,
            access=ACCESS_ALL,
            responses=Codes.responses(
                self.not_found_error_instance(),
                Codes.activation_email_resend,
                Codes.code_incorrect,
                Codes.already_active,
            ),
        )

    # email_change PATCH /me/email
    def _email_change_route(self) -> Callable[..., Any]:
        async def email_change(
                request: Request,
                background_tasks: BackgroundTasks,
                email: EmailStr = Body(...),
        ):
            user = cast(BaseUser, request.user)
            if user.email.lower() == email.lower():
                raise Codes.email_new_is_old.err()
            user_service = UserService(user)
            await user_service.raise_if_cant_change_email(new_email=email)
            background_tasks.add_task(user_service.send_email_change_email, new_email=email)
            return Codes.email_change_email.resp_detail(uuid=user.uuid)

        return email_change

    def _register_email_change(self) -> None:
        self.register_api_route(
            path='/me/email',
            endpoint=self._email_change_route(),
            methods=['PATCH'],
            summary='Email change',
            status_code=200,
            access=LOAD_USER,
            responses=Codes.responses(
                (Codes.email_change_email, {'uuid': uuid4()}),
                Codes.email_new_is_old,
                *UserService.cant_change_email_responses(),
                *Codes.auth_errors()
            )
        )

    # email_change_confirm GET /me/email/confirm
    def _email_change_confirm_route(self) -> Callable[..., Any]:
        async def email_change_confirm(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                uuid: Optional[UUID] = Query(None),
                code: str = Query(..., min_length=6, max_length=6)
        ):
            user = cast(BaseUser, request.user)
            user_repo = self.repo(request=request, background_tasks=background_tasks, response=response)
            if not user.is_authenticated:
                if not uuid:
                    raise self.not_found_error()
                try:
                    user = await user_repo.get_one(uuid, field_name='uuid')
                except ItemNotFound:
                    raise self.not_found_error()
            user_service = UserService(user)
            temp_code = await user_service.get_temp_code(trigger=TempCodeTriggers.EmailChange)
            if not temp_code:
                raise Codes.code_expired.err()
            new_email = temp_code.extras['new_email']
            await user_service.raise_if_cant_change_email(new_email=new_email)
            if temp_code_error := user_service.check_temp_code_error(code, temp_code):
                if temp_code_error == 'expired':
                    raise Codes.code_expired.err()
                else:
                    raise Codes.code_incorrect.err()
            await user_repo.edit(user, {'email': new_email})
            await user_service.delete_temp_code(temp_code)
            return Codes.email_changed.resp_detail(email=new_email)

        return email_change_confirm

    def _register_email_change_confirm(self) -> None:
        self.register_api_route(
            path='/me/email/confirm',
            endpoint=self._email_change_confirm_route(),
            methods=['GET'],
            summary='Confirm email change',
            status_code=200,
            access=LOAD_USER_OPTIONALLY,
            responses=Codes.responses(
                (Codes.email_changed, {'email': 'new-email@example.com'}),
                Codes.code_expired,
                Codes.code_incorrect,
                *UserService.cant_change_email_responses(),
                *Codes.auth_errors()
            )
        )

    # password_reset GET /me/password/reset
    def _password_reset_route(self) -> Callable[..., Any]:
        async def password_reset(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                username: str = Query(...)
        ):
            try:
                user = await self.repo(request=request, background_tasks=background_tasks, response=response)\
                    .get_one(username, field_name='username')
            except ItemNotFound:
                raise self.not_found_error()
            user_service = UserService(user)
            background_tasks.add_task(user_service.send_password_reset_email)
            return Codes.password_reset_email.resp_detail(uuid=user.uuid)

        return password_reset

    def _register_password_reset(self) -> None:
        self.register_api_route(
            path='/me/password/reset',
            endpoint=self._password_reset_route(),
            methods=['GET'],
            status_code=200,
            summary='Reset password',
            access=ACCESS_ALL,
            responses=Codes.responses(
                (Codes.password_reset_email, {'uuid': uuid4()}),
                self.not_found_error_instance(),
            )
        )

    # password_reset_confirm PATCH /me/password/reset/confirm
    def _password_reset_confirm_route(self) -> Callable[..., Any]:
        async def password_reset_confirm(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                uuid: Optional[UUID] = Query(...),
                code: str = Query(..., min_length=6, max_length=6),
                passwords: PasswordsPair = Body(...),
        ):
            try:
                user = await self.repo(request=request, background_tasks=background_tasks, response=response)\
                    .get_one(uuid, field_name='uuid')
            except ItemNotFound:
                raise self.not_found_error()
            user_service = UserService(user)
            temp_code = await user_service.get_temp_code(trigger=TempCodeTriggers.PasswordReset)
            if not temp_code:
                raise Codes.code_expired.err()
            if temp_code_error := user_service.check_temp_code_error(code, temp_code):
                if temp_code_error == 'expired':
                    raise Codes.code_expired.err()
                else:
                    raise Codes.code_incorrect.err()
            await user_service.update_password(passwords.password)
            await user_service.delete_temp_code(temp_code)
            return Codes.password_reset.resp

        return password_reset_confirm

    def _register_password_reset_confirm(self):
        self.register_api_route(
            path='/me/password/reset/confirm',
            endpoint=self._password_reset_confirm_route(),
            methods=['PATCH'],
            status_code=200,
            summary='Confirm reset password',
            access=ACCESS_ALL,
            responses=Codes.responses(
                Codes.password_reset,
                Codes.code_expired,
                Codes.code_incorrect,
                self.not_found_error_instance(),
            ),
        )

    # my_password_change PATCH /me/password
    def _my_password_change_route(self) -> Callable[..., Any]:
        async def my_password_change(
            request: Request,
            data: ChangePassword = Body(...)
        ):
            user = cast(BaseUser, request.user)
            user_service = UserService(user)
            if not user_service.verify_password(password=data.old_password):
                errors = ObjectErrors()
                errors.add('old_password', OldPasswordIsIncorrect)
                raise self.field_errors(errors)
            await user_service.update_password(data.password)
            return Codes.password_changed.resp

        return my_password_change

    def _register_my_password_change(self) -> None:
        self.register_api_route(
            path='/me/password',
            endpoint=self._my_password_change_route(),
            methods=['PATCH'],
            status_code=200,
            summary='Change my password',
            access=LOAD_USER,
            responses=Codes.responses(
                Codes.password_changed,
                self.field_errors_response_example({'oldPassword': OldPasswordIsIncorrect.key}),
                *Codes.auth_errors()
            )
        )

    # user_password_change PATCH /{user_id}/password
    def _user_password_change_route(self) -> Callable[..., Any]:
        async def user_password_change(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                user_id: PositiveInt = Path(...),
                data: PasswordsPair = Body(...)
        ):
            try:
                user = await self.repo(request=request, background_tasks=background_tasks, response=response) \
                    .get_one(user_id)
            except ItemNotFound:
                raise self.not_found_error()
            user_service = UserService(user)
            await user_service.update_password(data.password)
            return Codes.password_changed.resp

        return user_password_change

    def _register_user_password_change(self) -> None:
        self.register_api_route(
            path='/{user_id}/password',
            endpoint=self._user_password_change_route(),
            methods=['PATCH'],
            status_code=200,
            summary='Change other user password',
            access=CHECK_PERMS,
            permissions=('password_change',),
            responses=Codes.responses(
                Codes.password_changed,
                self.not_found_error_instance(),
                *Codes.auth_errors(),
                Codes.permission_denied,
            )
        )

    def EXTRA_names(self) -> tuple[str, ...]:
        return 'get_me', 'edit_me', 'registration', 'activation',\
            'email_change', 'email_change_confirm',\
            'password_reset', 'password_reset_confirm',\
            'my_password_change', 'user_password_change',
