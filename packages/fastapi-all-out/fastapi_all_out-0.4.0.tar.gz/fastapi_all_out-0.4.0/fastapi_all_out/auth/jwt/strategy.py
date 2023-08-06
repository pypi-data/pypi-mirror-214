from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional, Self

from jwt import PyJWT, InvalidSignatureError, DecodeError, ExpiredSignatureError

from fastapi_all_out.pydantic import CamelModel
from fastapi_all_out.responses import DefaultJSONEncoder
from fastapi_all_out.lazy_objects import get_schema, get_global_objects
from fastapi_all_out.enums import JWTTokenTypes
from fastapi_all_out.schemas import UserMeRead
from ..base import AuthStrategy, BaseUser
from .config import JWTAuthConfig
from .schemas import JWTToken, JWTTokenIssue


LIFETIME = dict[JWTTokenTypes, int]

JWTToken = get_schema(JWTToken)
JWTTokenIssue = get_schema(JWTTokenIssue)
UserMeRead = get_schema(UserMeRead)
Codes = get_global_objects().CODES


class TokenPair(CamelModel):
    access_token: str
    refresh_token: str
    user: UserMeRead
    token_type: str = 'bearer'

    class Config(CamelModel.Config):
        alias_generator = None


class JWTAuthStrategy(AuthStrategy):
    jwt = PyJWT()
    json_encoder = DefaultJSONEncoder

    authorize_response_model = TokenPair

    DECODE_SECRET: str
    ENCODE_SECRET: str
    SCHEMA: str

    def __init__(self, lifetime: LIFETIME, schema: str, encode_secret: str, decode_secret: str):
        self.lifetime = lifetime
        self.ENCODE_SECRET = encode_secret
        self.DECODE_SECRET = decode_secret
        self.SCHEMA = schema.lower()

    @property
    @abstractmethod
    def ALGORITHM(self) -> str: ...

    def decode(self, token: str) -> dict[str, Any]:
        return self.jwt.decode(token, self.DECODE_SECRET, [self.ALGORITHM])

    def encode(self, payload: dict[str, Any]) -> str:
        return self.jwt.encode(payload, self.ENCODE_SECRET, self.ALGORITHM, json_encoder=self.json_encoder)

    @staticmethod
    def now() -> int:
        return int(datetime.now().timestamp())

    def create_token(self, user, token_type: JWTTokenTypes, iat: int = None) -> str:
        return self.encode(
            JWTTokenIssue(
                user=user,
                type=token_type,
                iat=iat or self.now(),
                seconds=self.lifetime[token_type]
            ).dict()
        )

    def create_access_token(self, user: BaseUser, iat: int = None) -> str:
        return self.create_token(user, JWTTokenTypes.access, iat=iat)

    def create_refresh_token(self, user: BaseUser, iat: int = None) -> str:
        return self.create_token(user, JWTTokenTypes.refresh, iat=iat)

    def authorize(self, user: BaseUser) -> TokenPair:
        now = self.now()
        return TokenPair(
            access_token=self.create_access_token(user, iat=now),
            refresh_token=self.create_refresh_token(user, iat=now),
            user=user,
            token_type=self.SCHEMA.lower()
        )

    def get_token_payload(self, token: str):
        try:
            payload = self.decode(token)
        except (InvalidSignatureError, DecodeError):
            raise Codes.invalid_token.err()
        except ExpiredSignatureError:
            raise Codes.expired_token.err()
        return JWTToken(**payload)

    def parse_token(self, token: str, token_type: JWTTokenTypes) -> JWTToken:
        payload = self.get_token_payload(token)
        if payload.type != token_type:
            raise Codes.not_authenticated.err()
        return payload

    def get_access_token(self, token: Optional[str]) -> JWTToken:
        return self.parse_token(token, token_type=JWTTokenTypes.access)

    async def authenticate(self, token: Optional[str]) -> Optional[JWTToken]:
        if token is None:
            return None
        return self.get_access_token(token)

    def get_refresh_token(self, token: str) -> JWTToken:
        return self.parse_token(token, token_type=JWTTokenTypes.refresh)


class RS256JWTAuthStrategy(JWTAuthStrategy):
    ALGORITHM = 'RS256'

    @classmethod
    def from_config(cls, config: JWTAuthConfig) -> Self:
        return cls(
            lifetime={
                JWTTokenTypes.access: config.ACCESS_TOKEN_LIFETIME,
                JWTTokenTypes.refresh: config.REFRESH_TOKEN_LIFETIME,
            },
            schema=config.SCHEMA_NAME,
            encode_secret=config.RSA_PRIVATE.replace('|||n|||', '\n'),
            decode_secret=config.RSA_PUBLIC,
        )
