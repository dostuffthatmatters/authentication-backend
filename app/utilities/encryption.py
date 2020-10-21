
import hashlib
import secrets
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from fastapi import HTTPException, status

from app import pwd_context


def check_password_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        plain_password + os.getenv('PASSWORD_SALT'), hashed_password
    )


def generate_password_hash(password: str):
    return pwd_context.hash(password + os.getenv('PASSWORD_SALT'))


def generate_secret_token(length=32):
    return secrets.token_hex(length)


def generate_access_token(account):
    to_encode = {
        "email": account["email"],
        "email_verified": account["email_verified"],
        "exp": datetime.utcnow() + timedelta(
            minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
        )
    }
    encoded_jwt = jwt.encode(
        to_encode, os.getenv('SECRET_KEY'),
        algorithm=os.getenv('HASH_ALGORITHM')
    )
    return encoded_jwt


def check_access_token(access_token):
    try:
        payload = jwt.decode(
            access_token, os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('HASH_ALGORITHM')]
        )
        assert("exp" in payload)
        if datetime.fromtimestamp(payload["exp"]) < (datetime.utcnow() + timedelta(
            minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
        )):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        return payload
    except (AssertionError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


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
