import hashlib
import os
import ujson


def check_password_hash(user_password: str, password_hash: str) -> bool:
    """check plain password and hash password in db

    Args:
        user_password (str): [description]
        password_hash (str): [description]

    Returns:
        bool: `True` if plain password equal to hash else `False`
    """
    password_hash = ujson.loads(password_hash)
    salt, key = password_hash["salt"], password_hash["key"]
    new_key = hashlib.pbkdf2_hmac("sha256", user_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return key == new_key


def create_password_hash(user_password: str) -> dict:
    """[summary]

    Args:
        user_password (str): password in plain string

    Returns:
        dict: [description]
    """
    salt = os.urandom(32).hex()
    key = hashlib.pbkdf2_hmac("sha256", user_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return {"salt": salt, "key": key}
