
import os
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Form
from jose import jwt, JWTError

from app import account_collection

from app.utilities.encryption import generate_access_token, check_access_token, check_password_hash
from app.utilities.account_functions import get_account


async def authenticate_from_login(
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        account = await account_collection.find_one({"email": email})
        assert(account is not None)
        assert(check_password_hash(password, account["hashed_password"]))
        return generate_access_token(account)
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )


def authenticate_from_token(access_token: str):
    try:
        payload = check_access_token(access_token)
        account = get_account(email=payload["email"])
        assert(account is not None)
        return account
    except (AssertionError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
