
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app import app, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utilities.models import Token, User
from app.utilities.authenticating import authenticate_user, create_access_token, get_current_user


@app.get('/')
def index():
    return {"message": "Hello World"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data=user)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # This route requires the header:
    # 'Authorization: Bearer <token>'
    return current_user
