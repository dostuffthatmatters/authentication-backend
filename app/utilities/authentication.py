
import os
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Form
from jose import jwt, JWTError

from app import account_collection

from app.utilities.encryption import check_token, check_password_hash, \
    generate_access_token, generate_refresh_token
from app.utilities.account_functions import get_account


async def authenticate_from_login(
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        account = await account_collection.find_one({"email": email})
        assert(account is not None)
        assert(check_password_hash(password, account["hashed_password"]))
        return {
            "access_token": generate_access_token(account),
            "refresh_token": generate_refresh_token(account),
            "token_type": "bearer"
        }
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )


def authenticate_from_access_token(access_token: str):
    try:
        payload = check_token(access_token)
        account = get_account(email=payload["email"])
        assert(account is not None)
        return account
    except (AssertionError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def authenticate_from_refresh_token(refresh_token: str):
    try:
        payload = check_token(refresh_token)
        account = get_account(email=payload["email"])
        assert(account is not None)
        return generate_access_token(account)
    except (AssertionError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
