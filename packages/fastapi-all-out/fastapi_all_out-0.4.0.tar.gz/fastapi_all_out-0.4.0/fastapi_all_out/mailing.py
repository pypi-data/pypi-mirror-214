from typing import Any, TYPE_CHECKING
from pathlib import Path
from datetime import timedelta

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr, DirectoryPath, AnyHttpUrl

from fastapi_all_out.utils import timedelta_to_string

if TYPE_CHECKING:
    from fastapi_all_out.auth.base import BaseUser, TempCodeProto


class MailingConfig(ConnectionConfig):
    TEMPLATE_FOLDER: DirectoryPath = Path(__file__).parent / 'templates'

    HOST: AnyHttpUrl = 'http://localhost:8000'
    endpoints: dict[str, str] = {
        'activation': 'confirm',
        'email_change': 'email_change',
        'password_reset': 'password_reset',
    }
    temp_code_duration = {
        '_default': timedelta(hours=1),
    }


class MailSender:

    fast_mail: FastMail
    conf: MailingConfig

    def __init__(self, conf: "MailingConfig"):
        self.fast_mail = FastMail(conf)
        self.conf = conf

    async def send(
            self,
            to: EmailStr | str,
            data: dict[str, Any],
            template: str,
            subject: str
    ):
        email_msg = MessageSchema(
            subject=subject,
            recipients=[to],
            template_body=data,
            subtype=MessageType.html
        )
        await self.fast_mail.send_message(email_msg, template_name=template)

    async def send_tempcode_email(
            self,
            user: "BaseUser",
            temp_code: "TempCodeProto",
            host: str,
            endpoint: str,
            template: str,
            subject: str,
            **kwargs
    ) -> None:
        data = {
            'user': user, 'temp_code': temp_code, 'code': temp_code.code,
            'duration_text': timedelta_to_string(temp_code.duration),
            'host': host, 'endpoint': endpoint,
            **kwargs
        }
        await self.send(to=user.email, data=data, template=template, subject=subject)

    async def activation_email(self, user: "BaseUser", temp_code: "TempCodeProto") -> None:
        await self.send_tempcode_email(
            user=user,
            temp_code=temp_code,
            host=self.conf.HOST,
            endpoint=self.conf.endpoints['activation'],
            template='activation.html',
            subject='Account activation',
        )

    async def email_change_email(self, user: "BaseUser", temp_code: "TempCodeProto", new_email: str) -> None:
        await self.send_tempcode_email(
            user=user,
            temp_code=temp_code,
            host=self.conf.HOST,
            endpoint=self.conf.endpoints['email_change'],
            template='email_change.html',
            subject='Email change',
            new_email=new_email,
        )

    async def password_reset_email(self, user: "BaseUser", temp_code: "TempCodeProto") -> None:
        await self.send_tempcode_email(
            user=user,
            temp_code=temp_code,
            host=self.conf.HOST,
            endpoint=self.conf.endpoints['password_reset'],
            template='password_reset.html',
            subject='Password reset',
        )
