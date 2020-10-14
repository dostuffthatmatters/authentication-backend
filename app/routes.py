
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app.utilities.models import Token, Account, ModifiedAccount
from app.utilities.authenticating import \
    authenticate_from_login, authenticate_from_token
from app.utilities.accounting import create_account, verify_account, change_password

from app import app, ACCESS_TOKEN_EXPIRE_MINUTES, ENVIRONMENT


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


@app.put('/change-password')
async def change_password_route(
    access_token: str = Form(...),
    old_password: str = Form(...),
    new_password: str = Form(...)
):
    account = await authenticate_from_token(access_token)
    return await change_password(account, old_password, new_password)
