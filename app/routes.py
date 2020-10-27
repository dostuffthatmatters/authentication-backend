
from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app import app, ENVIRONMENT, PUBLIC_KEY, JWT_ALGORITHM, oauth2_scheme

from app.utilities.authentication import \
    authenticate_from_login, authenticate_from_access_token, \
    authenticate_from_refresh_token
from app.utilities.account_functions import change_password, \
    create_account, forgot_password, resend_verification, \
    restore_forgotten_password, verify_account
from app.utilities.encryption import generate_oauth_token
import time


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
        "status": "healthy",
        "mode": ENVIRONMENT,
        "public_key": PUBLIC_KEY,
        "jwt_algorithm": JWT_ALGORITHM
    }


@app.post("/login/form")
async def login_form_route(
    email: str = Form(...),
    password: str = Form(...)
):
    account = await authenticate_from_login(email, password)
    return {
        "oauth2_token": generate_oauth_token(account),
        "account": account
    }


@app.post("/login/access")
async def login_access_token_route(
    access_token: str = Form(...)
):
    # Don't need to generate a new jwt when the access_token is still valid
    account = await authenticate_from_access_token(access_token)
    return {
        "account": account
    }


@app.post("/login/refresh")
async def login_refresh_token_route(
    refresh_token: str = Form(...)
):
    account = await authenticate_from_refresh_token(refresh_token)
    return {
        "oauth2_token": generate_oauth_token(account),
        "account": account
    }


@app.post('/register')
async def register_route(
    email: str = Form(...),
    password: str = Form(...)
):
    account = await create_account(email, password)
    return {
        "oauth2_token": generate_oauth_token(account),
        "account": account
    }


@app.post('/verify')
async def verify_route(
    email_token: str = Form(...),
    password: str = Form(...)
):
    account = await verify_account(email_token, password)
    return {
        "oauth2_token": generate_oauth_token(account),
        "account": account
    }


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


@app.post('/request-new-password')
async def change_password_route(
    email: str = Form(...)
):
    return await forgot_password(email)


@app.post('/set-new-password')
async def change_password_route(
    password_token: str = Form(...),
    password: str = Form(...)
):
    account = await restore_forgotten_password(password_token, password)
    return {
        "oauth2_token": generate_oauth_token(account),
        "account": account
    }


@app.post('/resend-verification')
async def change_password_route(
    email: str = Form(...),
):
    await resend_verification(email)
    return {"status": "success"}
