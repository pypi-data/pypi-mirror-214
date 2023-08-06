from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer

from fastapi_all_out.pydantic import ConfigModel


class JWTAuthConfig(ConfigModel):

    # for RS256JWTAuthStrategy
    RSA_PRIVATE: str = None
    RSA_PUBLIC: str = None
    ACCESS_TOKEN_LIFETIME: int = int(timedelta(minutes=5).total_seconds())
    REFRESH_TOKEN_LIFETIME: int = int(timedelta(days=30).total_seconds())

    # for JWTOAuth2PasswordBearerBackend
    SCHEMA_NAME: str = 'bearer'
    TOKEN_URL: str = '/api/auth/jwt/login'
    AUTO_ERROR: bool = False

    def get_oauth2_password_bearer(self):
        return OAuth2PasswordBearer(
            tokenUrl=self.TOKEN_URL,
            scheme_name=self.SCHEMA_NAME,
            auto_error=self.AUTO_ERROR
        )
