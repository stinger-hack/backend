from datetime import datetime
import uuid
import ujson
from services.db import DB


async def get_password(email: str) -> dict:
    query = f"""
        select user_password
        from users
        where email = '{email}'
    """
    return await DB.conn.fetchval(query)


async def register_user(user_id: str, first_name: str, email: str, user_password: dict) -> None:
    query = """
        insert into users (user_id, email, first_name, user_password, created_at)
        values ($1, $2, $3, $4, $5)
    """
    await DB.conn.execute(query, user_id, email, first_name, ujson.dumps(user_password), datetime.now())


async def user_from_login(email: str) -> str:
    query = """
        select user_id
        from users
        where email = $1
    """
    user_id = await DB.conn.fetchval(query, email)
    return user_id.hex


async def user_from_email(email: str) -> str:
    query = """
        select user_id
        from user
        where email = $1
    """
    user_id = await DB.conn.fetchval(query, email)
    return user_id.hex


async def user_exist(email: str) -> str:
    query = """
        select exists (
            select
            from users
            where email = $1
        )
    """
    return await DB.conn.fetchval(query, email)


async def get_temp_password(email: str) -> str:
    query = """
       select temp_password
       from users
       where email = $1
    """
    return await DB.conn.fetchval(query, email)


async def set_new_password(new_password_hash: dict, email: str) -> None:
    query = """
       update users
          set
             user_password = $1
             temp_password = NULL
       where email = $2
    """
    await DB.conn.execute(query, ujson.dumps(new_password_hash), email)


async def set_temp_password(new_password_hash: dict, email: str, device_id: str) -> None:
    is_user = await user_exist(email)
    if is_user:
        await update_temp_password(ujson.dumps(new_password_hash), email)
    else:
        query = """
        insert into users (user_id, email, temp_password, device_id, created_at)
        select $1, $2, $3, $4, $5
        where not exists (
            select
            from users
            where email = $2::varchar
        )
        """
        await DB.conn.execute(query, uuid.uuid4(), email, ujson.dumps(new_password_hash), device_id, datetime.now())


async def update_temp_password(code: str, email: str) -> None:
    query = """
       update users
       set
          temp_password = $1
       where email = $2
    """
    await DB.conn.execute(query, code, email)


async def update_user_data(first_name: str, password: dict, email: str) -> None:
    query = """
       update users
       set
          user_password = $1,
          first_name = $2
       where email = $3
    """
    await DB.conn.execute(query, ujson.dumps(password), first_name, email)
