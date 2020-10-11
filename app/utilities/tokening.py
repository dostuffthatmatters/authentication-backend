
import secrets
from datetime import datetime, timedelta
from jose import jwt
from app.utilities.models import Account

from app import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, HASH_ALGORITHM


def generate_secret_token(length=32):
    return secrets.token_hex(length)


def create_access_token(account: Account):
    to_encode = account.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt
