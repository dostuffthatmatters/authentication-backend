
from typing import Optional
from fastapi import HTTPException, status, Response

from app import account_collection

from app.utilities.encryption import check_password_hash, generate_oauth_token, generate_password_hash, generate_secret_token, validate_password_format
from app.utilities.mailing import \
    send_verification_mail, send_forgot_password_mail
import os


async def get_account(email: str):
    return await account_collection.find_one(
        {"email": email}, {"_id": 0, "email": 1, "email_verified": 1}
    )


async def create_account(email: str, password: str):

    if not validate_password_format(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="password format invalid",
        )

    account_model = {
        "email": email,
        "hashed_password": generate_password_hash(password),
        "email_token": generate_secret_token(length=32),
        "email_verified": False
    }

    try:
        # collection has a unique index on "email"
        # -> trying to insert a mail that already exists
        # will result in an error
        await account_collection.insert_one(account_model)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already taken",
        )

    try:
        await send_verification_mail(account_model)
    except AssertionError:
        await account_collection.delete_one({"email": email})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"verification email could not be sent",
        )

    return {"email": email, "email_verified": False}


async def verify_account(email_token: str, password: str):
    try:
        account = await account_collection.find_one(
            {"email_token": email_token},
            {"_id": 0, "hashed_password": 1}
        )
        assert(account is not None)
        assert(check_password_hash(password, account["hashed_password"]))
        await account_collection.update_one(
            {"email_token": email_token},
            {'$set': {'email_verified': True}}
        )
        return {"status": "success"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email_token or password invalid",
        )


async def change_password(account, old_password, new_password):
    if not account["email_verified"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email address not verified yet",
        )

    if not validate_password_format(new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new_password format invalid",
        )

    db_account = await account_collection.find_one(
        {"email": account["email"]},
        {"_id": 0, "hashed_password": 1}
    )

    if not check_password_hash(old_password, db_account["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="old_password invalid",
        )

    await account_collection.update_one(
        {"email": account["email"]},
        {"$set": {"hashed_password": generate_password_hash(new_password)}}
    )

    return {"status": "success"}


async def forgot_password(email: str):

    token = generate_secret_token(length=32)

    await account_collection.update_one(
        {"email": email},
        {"$set": {
            "forgot_password_token": token,
        }}
    )

    # 500 Error if mail cannot be sent
    # 400 not possible since the email should be valid
    await send_forgot_password_mail(email, token)

    return {"status": "success"}


async def restore_forgotten_password(forgot_password_token, new_password):

    if not validate_password_format(new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new_password format invalid",
        )

    account = await account_collection.find_one(
        {"forgot_password_token": forgot_password_token},
        {"_id": 0}
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="forgot_password_token invalid",
        )

    await account_collection.update_one(
        {"forgot_password_token": forgot_password_token},
        {'$set': {'hashed_password': generate_password_hash(new_password)},
         '$unset': {'forgot_password_token': 1}}
    )
    return {"status": "success"}
