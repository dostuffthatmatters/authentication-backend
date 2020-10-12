
from typing import Optional
from fastapi import HTTPException, status

from app import account_collection
from app.utilities.hashing import generate_password_hash
from app.utilities.tokening import generate_secret_token
from app.utilities.models import AccountInDB
from app.utilities.validating import validate_password_format


async def get_account(email: str):
    account: Optional[AccountInDB] = \
        await account_collection.find_one({"email": email})
    return {'email': account["email"], "email_verified": account["email_verified"]}


async def create_account(email: str, password: str):

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

    try:
        # collection has a unique index on "email"
        await account_collection.insert_one(account_model)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken",
        )

    # TODO: Send verification mail

    return {
        "email": email,
        "email_verified": False
    }
