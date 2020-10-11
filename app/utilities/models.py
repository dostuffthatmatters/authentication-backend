
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class User(BaseModel):
    email: str


class UserInDB(BaseModel):
    email: str
    hashed_password: str
