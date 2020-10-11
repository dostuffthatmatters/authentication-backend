
from fastapi import Depends, FastAPI, HTTPException, status, Form
from datetime import datetime, timedelta

from app import app, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utilities.models import Token, User
from app.utilities.authenticating import authenticate_user, create_access_token, get_current_user


@app.get('/')
def index():
    return {"message": "Hello World"}


@app.post("/login", response_model=Token)
def login_for_access_token(
    email: str = Form(...),
    password: str = Form(...)
):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data=user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=User)
def profile(current_user: User = Depends(get_current_user)):
    # This route requires the form-data to include:
    # 'access_token': '...'
    return current_user
