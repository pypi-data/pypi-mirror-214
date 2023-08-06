from enum import Enum
from itertools import groupby
from types import DynamicClassAttribute
from typing import Any, Type , Union

from fastapi import BackgroundTasks

from fastapi_all_out.pydantic import CamelModel, lower_camel
from fastapi_all_out.responses import BgHTTPException


class CodeResponse(CamelModel):
    code: str
    message: str


class BaseCodes(Enum):
    """Example
        # normal
        email_activation_link_send = 200, 'Activation link was sent to your email',
        activation_completed = 200, 'Activation completed successfully',
        # errors
        email_exist = 400, 'User with such email is already exists'
        phone_exist = 400, 'User with such phone number is already exists'
        username_exist = 400, 'User with such username is already exists'
        incorrect_link = 400, 'Your link is incorrect or expired'
        email_active = 400, 'Your email is already active'
        private_completed = 400, 'Your private info is already completed'
        footballer_completed = 400, 'Your footballer info is already completed'
    """

    @DynamicClassAttribute
    def value(self) -> tuple:
        return self._value_

    @property
    def status(self) -> int:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]

    @property
    def headers(self):
        return self.value[2] if len(self.value) > 2 else None

    @property
    def resp(self) -> dict[str, Any]:
        return {'code': lower_camel(self.name), 'message': self.message}

    def format_resp(self, values: str | tuple[str]):
        values = (values,) if isinstance(values, str) else values
        return {'code': lower_camel(self.name), 'message': self.message.format(*values)}

    @property
    def error_class(self) -> Type[BgHTTPException]:
        return BgHTTPException

    def err(self, details: dict[str, Any] = None, background: BackgroundTasks = None) -> BgHTTPException:
        resp = {**self.resp, **details} if details else self.resp
        return self.error_class(self.status, detail=resp, headers=self.headers, background=background)

    def format_err(self, values: str | tuple[str], details: dict[str, Any] = None, background: BackgroundTasks = None):
        resp = {**self.format_resp(values), **details} if details else self.format_resp(values)
        return self.error_class(self.status, detail=resp, headers=self.headers, background=background)

    def resp_detail(self, **kwargs) -> dict[str, Any]:
        return {**self.resp, **kwargs}

    @classmethod
    def responses(
            cls,
            *codes: Union["BaseCodes", tuple["BaseCodes", dict[str, Any]]],
    ) -> dict[int, dict[str, Any]]:

        def key(x: BaseCodes | tuple[BaseCodes, dict[str, Any]]):
            if isinstance(x, tuple):
                x = x[0]
            return x.status

        grouped_responses = groupby(sorted(codes, key=key), key=key)
        responses = {}
        for status, codes in grouped_responses:
            codes = tuple(codes)
            if len(codes) > 1:
                examples = {}
                for code in codes:
                    if isinstance(code, tuple):
                        examples[lower_camel(code[0].name)] = {'value': code[0].resp_detail(**code[1])}
                    else:
                        examples[lower_camel(code.name)] = {'value': code.resp_detail()}
                example = {'examples': examples}
            else:
                code = codes[0]
                if isinstance(code, tuple):
                    example = {'example': code[0].resp_detail(**code[1])}
                else:
                    example = {'example': code.resp_detail()}
            responses[status] = {
                "model": CodeResponse,
                "content": {
                    "application/json": example
                },
            }
        return responses


class DefaultCodes(BaseCodes):
    OK = 200, 'ОК'
    not_found = 404, 'Item not found.'
    fields_error = 400, 'Fix all fields errors.'

    code_incorrect = 400, 'Code is incorrect.'
    code_expired = 400, 'Code is expired.'

    activation_email = 201, 'We sent activation code to your email.\nCheck spam if you can`t find it.'
    activation_email_resend = 400, 'Your activation code is expired, we sent new one to your email.\n' \
                                   'Check spam if you can`t find it.'
    activation_email_check = 400, 'Check code on your email.\nCheck spam if you can`t find it.'
    already_active = 400, 'You are already active.\nTry to sign in.'

    email_change_email = 200, 'We sent confirmation code to your email.\nCheck spam if you can`t find it.'
    email_changed = 200, 'Email changed successfully'
    email_new_is_old = 400, 'New email is equal to old one.'

    password_changed = 200, 'Password changed successfully.'
    password_reset = 200, 'Password reset successfully.'
    password_reset_email = 200, 'We sent password change link to your email.\nCheck spam if you can`t find it.'

    invalid_token = 401, "Authorization token is incorrect"
    expired_token = 401, "Authorization is expired"
    not_authenticated = 401, "Not authenticated"
    permission_denied = 403, "Permission denied"

    @classmethod
    def auth_errors(cls) -> tuple:
        return cls.invalid_token, cls.expired_token, cls.not_authenticated
