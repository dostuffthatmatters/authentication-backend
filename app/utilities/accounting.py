
from app.utilities.hashing import generate_password_hash
from app.utilities.tokening import generate_secret_token


def get_account(email: str):
    # 1. Find user with email
    # 2. Return user model or Nothing
    return {'email': 'abc@de.fg', "email_verified": False}


def create_account(email: str, password: str):
    # TODO: Check if email has already been taken
    # TODO: Check if password has the correct format

    account_model = {
        "email": email,
        "hashed_password": generate_password_hash(password),
        "email_token": generate_secret_token(length=32),
        "email_verified": False
    }

    # TODO: Send verification mail
    # TODO: Save user to database

    return {
        "email": email,
        "email_verified": False
    }
