import random
from fastapi import Request
from fastapi.responses import UJSONResponse
from fastapi.routing import APIRouter
from queries.login import (
    get_temp_password,
    set_temp_password,
    update_user_data,
    user_from_email
)
from services.jwt_auth import AccessTokenPayload, create_token
from utils.password import check_password_hash, create_password_hash

from routes.schema.login import (
    UserPhoneCodeSchema,
    UserPhoneSchema
)
from utils.sms import send_sms

phone_login_router = APIRouter(prefix="/phone")


@phone_login_router.post("/login", description="Ввод номера телефона")
async def phone_login_route(request: Request, body: UserPhoneSchema) -> UJSONResponse:
    req: dict = await request.json()
    phone = req.get("phone")
    device_id = req.get("device_id")
    if phone != "79999999999" and phone != "+79999999999":  # harcode number for faster testing
        code = str(random.randint(1000, 9999))
        password_hash = create_password_hash(code)
        send_sms(phone, code)
        await set_temp_password(password_hash, phone, device_id)


@phone_login_router.post("/confirm", description="Ввод кода из смс")
async def phone_confirm_route(request: Request, body: UserPhoneCodeSchema) -> UJSONResponse:
    req: dict = await request.json()
    code = req.get("code")
    phone = req.get("phone")
    db_password_hash = await get_temp_password(phone)
    if check_password_hash(code, db_password_hash):
        user_id = await user_from_email(phone)
        access_payload = AccessTokenPayload(sub=user_id, phone=phone)
        token = create_token(access_payload)
        return token


@phone_login_router.post("/complete_reg", description="Задание пароля и имени")
async def complete_reg_route(request: Request) -> None:
    req: dict = await request.json()
    first_name = req.get("first_name")
    password = req.get("password")
    phone = req.get("phone")
    password_hash = create_password_hash(password)
    await update_user_data(first_name, password_hash, phone)
