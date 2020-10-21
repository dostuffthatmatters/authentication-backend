
from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app import app, ENVIRONMENT, PUBLIC_KEY, oauth2_scheme

from app.utilities.authentication import \
    authenticate_from_login, authenticate_from_access_token, \
    authenticate_from_refresh_token
from app.utilities.account_functions import \
    create_account, verify_account, change_password, \
    forgot_password, restore_forgotten_password


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class Account(BaseModel):
    email: str
    email_verified: bool


@app.get('/')
def index_route():
    return {
        "status": "running",
        "mode": ENVIRONMENT,
        "public_key": PUBLIC_KEY
    }


@app.post("/login", response_model=Token)
async def login_route(
    email: str = Form(...),
    password: str = Form(...)
):
    return await authenticate_from_login(email, password)


@app.post("/refresh", response_model=Token)
async def login_route(
    refresh_token: str = Form(...)
):
    return await authenticate_from_refresh_token(refresh_token)


@app.post('/register', response_model=Token)
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


@app.get("/account", response_model=Account)
async def account_route(
    access_token: str = Depends(oauth2_scheme)
):
    return await authenticate_from_access_token(access_token)


@app.post('/change-password')
async def change_password_route(
    access_token: str = Depends(oauth2_scheme),
    old_password: str = Form(...),
    new_password: str = Form(...)
):
    account = await authenticate_from_access_token(access_token)
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
