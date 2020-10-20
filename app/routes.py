
from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app import app, ENVIRONMENT

from app.utilities.authentication import \
    authenticate_from_login, authenticate_from_token
from app.utilities.account_functions import \
    create_account, verify_account, change_password, \
    forgot_password, restore_forgotten_password


class Token(BaseModel):
    access_token: str
    token_type: str


class Account(BaseModel):
    email: str
    email_verified: bool


@app.get('/')
def index_route():
    return {
        "status": "running",
        "mode": ENVIRONMENT
    }


@app.post("/login", response_model=Token)
async def login_route(
    email: str = Form(...),
    password: str = Form(...)
):
    access_token = await authenticate_from_login(email, password)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/register', response_model=Account)
async def register_route(
    email: str = Form(...),
    password: str = Form(...)
):
    return await create_account(email, password)


@app.post('/verify')
async def verify_route(
    email_token: str = Form(...),
    password: str = Form(...)
):
    return await verify_account(email_token, password)


# POST and not a GET request because a GET request:
# 1. might get cached
# 2. does not have a body (no TLS encryption on the token)
@app.post("/account", response_model=Account)
async def account_route(
    access_token: str = Form(...)
):
    return await authenticate_from_token(access_token)


@app.post('/change-password')
async def change_password_route(
    access_token: str = Form(...),
    old_password: str = Form(...),
    new_password: str = Form(...)
):
    account = await authenticate_from_token(access_token)
    return await change_password(account, old_password, new_password)


@app.post('/forgot-password')
async def change_password_route(
    email: str = Form(...)
):
    return await forgot_password(email)


@app.post('/restore-forgotten-password')
async def change_password_route(
    forgot_password_token: str = Form(...),
    new_password: str = Form(...)
):
    return await restore_forgotten_password(forgot_password_token, new_password)
