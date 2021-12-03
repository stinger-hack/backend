from pydantic import BaseModel

EMAIL_EXAMPLE = "username@email.com"
PHONE_EXAMPLE = "+79998887766"


class UserRegisterSchema(BaseModel):
    first_name: str
    email: str = EMAIL_EXAMPLE
    password: str


class UserLoginSchema(BaseModel):
    email: str = EMAIL_EXAMPLE
    password: str


class UserPhoneSchema(BaseModel):
    phone: str
    device_id: str


class UserPhoneCodeSchema(BaseModel):
    phone: str
    code: str


class UserCompleteSchema(BaseModel):
    password: str
    first_name: str
    phone: str


class LocationSchema(BaseModel):
    lat: float
    long: float


class TempPasswordSchema(BaseModel):
    email: str = EMAIL_EXAMPLE


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
