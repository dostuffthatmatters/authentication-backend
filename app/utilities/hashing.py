import hashlib
from app import PASSWORD_SALT, pwd_context


def check_password_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password + PASSWORD_SALT, hashed_password)


def generate_password_hash(password: str):
    return pwd_context.hash(password + PASSWORD_SALT)
