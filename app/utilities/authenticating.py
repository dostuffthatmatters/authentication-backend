
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Form
from jose import jwt, JWTError

from app import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, HASH_ALGORITHM
from app.utilities.tokening import create_access_token
from app.utilities.accounting import get_account


def authenticate_from_login(
    email: str = Form(...),
    password: str = Form(...)
):
    # 1. Find user with email
    # 2. If no user -> return False
    account = {
        'email': 'abc@de.fg',
        'email_verified': False
    }

    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Check if password matches
    # 4. If not match -> return False
    # 5. Return user model
    return create_access_token(account)


def authenticate_from_token(
    access_token: str = Form(...)
):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        email: str = payload.get("email")
        assert(email is not None)
        account = get_account(email=email)
        assert(account is not None)
        return account
    except (AssertionError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
