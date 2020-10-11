
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Form
from jose import jwt, JWTError

from app import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, HASH_ALGORITHM


def authenticate_user(email: str, password: str):
    # 1. Find user with email
    # 2. If no user -> return False
    # 3. Check if password matches
    # 4. If not match -> return False
    # 5. Return user model
    return {'email': 'abc@de.fg'}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


def get_user(email: str):
    # 1. Find user with email
    # 2. Return user model or Nothing
    return {'email': 'abc@de.fg'}


def get_current_user(access_token: str = Form(...)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        email: str = payload.get("email")
        assert(email is not None)
        user = get_user(email=email)
        assert(user is not None)
        return user
    except (AssertionError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
