
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class Account(BaseModel):
    email: str
    email_verified: bool


class AccountInDB(Account):
    hashed_password: str
    email_token: str
