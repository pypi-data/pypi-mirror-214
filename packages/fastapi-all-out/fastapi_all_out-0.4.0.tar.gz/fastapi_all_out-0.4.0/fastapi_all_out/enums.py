from enum import Enum


class Databases(Enum):
    tortoise = 'tortoise'


class TempCodeTriggers(Enum):
    EmailActivation = 'EA'
    EmailChange = 'EC'
    PasswordReset = 'PR'


class JWTTokenTypes(Enum):
    access = 'access'
    refresh = 'refresh'
