
from typing import Optional
from fastapi import HTTPException, status

from app import account_collection
from app.utilities.hashing import generate_password_hash
from app.utilities.tokening import generate_secret_token
from app.utilities.models import AccountInDB
from app.utilities.validating import validate_password_format


def get_account(email: str):
    # 1. Find user with email
    # 2. Return user model or Nothing
    return {'email': 'abc@de.fg', "email_verified": False}


async def create_account(email: str, password: str):

    existing_account: Optional[AccountInDB] = \
        await account_collection.find_one({"email": email})

    if existing_account is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken",
        )

    if not validate_password_format(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password format invalid",
        )

    account_model = {
        "email": email,
        "hashed_password": generate_password_hash(password),
        "email_token": generate_secret_token(length=32),
        "email_verified": False
    }

    # TODO: Send verification mail

    account_collection.insert_one(account_model)

    return {
        "email": email,
        "email_verified": False
    }
