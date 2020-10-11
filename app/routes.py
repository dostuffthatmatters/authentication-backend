
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app.utilities.models import Token, Account
from app.utilities.authenticating import \
    authenticate_from_login, authenticate_from_token
from app.utilities.accounting import create_account

from app import app, ACCESS_TOKEN_EXPIRE_MINUTES


@app.get('/')
def index():
    return {"message": "Hello World"}


@app.post("/login", response_model=Token)
def login_for_access_token(access_token: Token = Depends(authenticate_from_login)):
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/account", response_model=Account)
def profile(account: Account = Depends(authenticate_from_token)):
    # This route requires the form-data to include:
    # 'access_token': '...'
    return account


@app.post('/register', response_model=Account)
def register(
    email: str = Form(...),
    password: str = Form(...)
):
    create_account(email, password)
    return {"email": "Gok World"}