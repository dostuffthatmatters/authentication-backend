import hashlib
from app import PASSWORD_SALT, pwd_context


import secrets
from datetime import datetime, timedelta
from jose import jwt

from app import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, HASH_ALGORITHM


def check_password_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password + PASSWORD_SALT, hashed_password)


def generate_password_hash(password: str):
    return pwd_context.hash(password + PASSWORD_SALT)


def generate_secret_token(length=32):
    return secrets.token_hex(length)


def create_access_token(account):
    to_encode = {"email": account["email"], "email_verified": account["email_verified"]}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


def validate_password_format(password: str):
    try:
        assert(8 <= len(password))
        assert(len(password) <= 32)
        assert(any([c.isnumeric() for c in password]))
        assert(any([c.isalpha() for c in password]))
        assert(any([not (c.isnumeric() or c.isalpha()) for c in password]))
        return True
    except AssertionError:
        return False

# Validating the Email format here is useless ;)
