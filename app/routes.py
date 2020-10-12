
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app.utilities.models import Token, Account
from app.utilities.authenticating import \
    authenticate_from_login, authenticate_from_token
from app.utilities.accounting import create_account, verify_account

from app import app, ACCESS_TOKEN_EXPIRE_MINUTES, ENVIRONMENT


@app.get('/')
def index():
    return {
        "status": "running",
        "mode": ENVIRONMENT
    }


@app.post("/login", response_model=Token)
async def login_for_access_token(
    email: str = Form(...),
    password: str = Form(...)
):
    access_token = await authenticate_from_login(email, password)
    return {"access_token": access_token, "token_type": "bearer"}


# POST and not a GET request because a GET request:
# 1. might get cached
# 2. does not have a body (no TLS encryption on the token)
@app.post("/account", response_model=Account)
async def profile(
    access_token: str = Form(...)
):
    return await authenticate_from_token(access_token)


@app.post('/register', response_model=Account)
async def register(
    email: str = Form(...),
    password: str = Form(...)
):
    return await create_account(email, password)


@app.post('/verify')
async def register(
    email_token: str = Form(...),
    password: str = Form(...)
):
    return await verify_account(email_token, password)
