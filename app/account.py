
from typing import Optional
from fastapi import HTTPException, status, Response

from app import account_collection

from app.utilities.encryption import check_password_hash, generate_oauth_token, generate_password_hash, generate_secret_token, validate_password_format
from app.utilities.mailing import \
    send_verification_mail, send_forgot_password_mail
import os






import secrets

from pymongo.errors import DuplicateKeyError
from datetime import datetime



class AccountManager:
    """The AccountManager manages creating/updation/deleting accounts."""

    def __init__(self, database):
        """Initialize an account manager instance."""
        self.unverified = database['authentication.accounts.unverified']
        self.verified = database['authentication.accounts.verified']
        self.unverified.create_index(
            keys='timestamp',
            name='timestamp-index',
            # delete unverified (draft) accounts after 10 minutes
            expireAfterSeconds=10*60,
        )

    async def fetch(self, email: str):
        """Fetch an account given its primary key."""
        return await self.verified.find_one(
            filter={'email': email},
            projection={'_id': False},
        )

    async def create(self, email: str, password: str):
        """Create a new account in the database."""

        # TODO implement real validator that also checks for email maxlength
        # and type with better error reporting

        if not validate_password_format(password):
            raise HTTPException(400, 'invalid password format')

        # TODO search for own primary key instead of using the email

        check = await self.verified.find_one(
            filter={'email': email},
            projection={'_id': False, 'pwdhash': False},
        )
        if check is not None:
            raise HTTPException(400, 'email already taken')

        unverified_account = {
            '_id': secrets.token_hex(64),
            'email': email,
            'pwdhash': generate_password_hash(password),
            'created': datetime.utcnow(),
        }
        while True:
            try:
                await self.unverified.insert_one(unverified_account)
                break
            except DuplicateKeyError:
                unverified_account['_id'] = secrets.token_hex(64)

        # TODO replace AssertionErrors with meaningful exceptions
        # how do we deal with mailing errors when entries get deleted anyways?

        try:
            await send_verification_mail(unverified_account)
        except AssertionError:
            await self.unverified.delete_one({'email': email})
            raise HTTPException(

                # TODO is this the right status code?

                status_code=status.HTTP_400_BAD_REQUEST,
                detail='verification email could not be sent',
            )

        return {'email': email, 'verified': False}

    async def verify(self, token: str, password: str):
        """Verify an existing account via its unique verification token."""
        unverified_account = await self.unverified.find_one(
            filter={'_id': token},
            projection={'_id': False, 'created': False},
        )
        if unverified_account is None:
            raise HTTPException(401, 'invalid token')
        if not check_password_hash(password, unverified_account['pwdhash']):
            raise HTTPException(401, 'invalid password')
        verified_account = {

            # TODO create own primary key instead of using the email

            'email': unverified_account['email'],
            'pwdhash': unverified_account['pwdhash'],
            'created': datetime.utcnow(),
        }
        await self.verified.insert_one(verified_account)
        await self.unverified.delete_one(filter={'_id': token})
        return {'email': verified_account['email'], 'verified': True}

    async def update(self):
        """Update an existing account in the database."""
        raise HTTPException(501, 'not yet implemented')

    async def delete(self):
        """Delete all data of an existing account."""
        raise HTTPException(501, 'not yet implemented')



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
        "email_token": generate_secret_token(length=20),
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
            {"email_token": email_token}
        )
        assert(account is not None)
        assert(check_password_hash(password, account["hashed_password"]))
        await account_collection.update_one(
            {"email_token": email_token},
            {'$set': {'email_verified': True}}
        )
        return {
            "email": account["email"],
            "email_verified": True
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
            "password_token": token,
        }}
    )

    # 500 error if email cannot be sent
    await send_forgot_password_mail(email, token)

    return {"status": "success"}


async def restore_forgotten_password(password_token, new_password):

    if not validate_password_format(new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new_password format invalid",
        )

    account = await account_collection.find_one(
        {"password_token": password_token},
        {"_id": 0, "email": 1, "email_verified": 1}
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password_token invalid",
        )

    await account_collection.update_one(
        {"password_token": password_token},
        {'$set': {'hashed_password': generate_password_hash(new_password)},
         '$unset': {'password_token': 1}}
    )
    return account


async def resend_verification(email):
    account = await account_collection.find_one({"email": email})

    if account is not None:
        # 500 error if email cannot be sent
        await send_verification_mail(account)
