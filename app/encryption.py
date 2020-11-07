
import hashlib
import secrets
from datetime import datetime, timedelta
import jwt
import os
from fastapi import HTTPException, status

from app import pwd_context, JWT_ALGORITHM, PRIVATE_KEY, PUBLIC_KEY, \
    PASSWORD_SALT, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME


def check_password_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        plain_password + PASSWORD_SALT, hashed_password
    )


def generate_password_hash(password: str):
    return pwd_context.hash(password + PASSWORD_SALT)


def generate_secret_token(length=32):
    return secrets.token_hex(length)


def generate_oauth_token(account):
    return {
        "access_token": generate_jwt(
            {"email": account["email"], "email_verified": False},
            ACCESS_TOKEN_LIFETIME
        ),
        "refresh_token": generate_jwt(
            {"email": account["email"], "email_verified": False},
            REFRESH_TOKEN_LIFETIME
        ),
        "token_type": "bearer"
    }


def generate_jwt(account, token_lifetime):
    to_encode = {
        "email": account["email"],
        "email_verified": account["email_verified"],
        "exp": datetime.utcnow() + timedelta(
            seconds=token_lifetime
        )
    }
    return jwt.encode(
        to_encode, PRIVATE_KEY,
        algorithm=JWT_ALGORITHM
    ).decode('utf-8')


def check_jwt(token):
    try:
        payload = jwt.decode(
            token, PUBLIC_KEY,
            algorithms=JWT_ALGORITHM
        )
        assert("exp" in payload)
        if payload["exp"] < datetime.timestamp(datetime.utcnow()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        return payload
    except (AssertionError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def validate_password_format(password: str):
    return (
        type(password) == str
        and 8 <= len(password) <= 512
    )
