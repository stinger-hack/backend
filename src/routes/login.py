import uuid
from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse
from queries.login import (
    get_password,
    register_user,
    user_exist,
    user_from_login,
)
from services.jwt_auth import AccessTokenPayload, create_token
from utils.password import check_password_hash, create_password_hash

from routes.schema.login import (
    UserLoginSchema,
    UserRegisterSchema
)

login_router = APIRouter(prefix="/user")



@login_router.post("/login")
async def login(request: Request, body: UserLoginSchema) -> UJSONResponse:
    req: dict = await request.json()
    email = req.get("email")
    user_password = req.get("password")

    password_hash = await get_password(email)

    if not password_hash:
        return UJSONResponse(status_code=409, content={"message": f"User with email {email} doesn't exist"})

    if check_password_hash(user_password, password_hash):
        user_id = await user_from_login(email)
        access_payload = AccessTokenPayload(sub=user_id, email=email)
        token = create_token(access_payload)
        return token

    return UJSONResponse(status_code=400, content={"message": "The user_password or email does not match"})


@login_router.post("/registration")
async def registration(request: Request, body: UserRegisterSchema) -> str:
    req: dict = await request.json()
    email = req.get("email")
    user_password = req.get("password")
    first_name = req.get("first_name")

    password_hash = create_password_hash(user_password)

    is_user_exist = await user_exist(email)

    if is_user_exist:
        return UJSONResponse(status_code=409, content={"message": f"User with email {email} already exist"})

    try:
        user_id = uuid.uuid4().hex
        access_payload = AccessTokenPayload(sub=user_id)
        token = create_token(access_payload)
    except ValueError:
        return "Token Error"

    await register_user(user_id, first_name, email, password_hash)
    return token
