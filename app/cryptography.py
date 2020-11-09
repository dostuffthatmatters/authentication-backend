import jwt
import os

from passlib.context import CryptContext
from jwt import ExpiredSignatureError
from datetime import datetime, timedelta


class PasswordManager:
    """The PasswordManager manages hashing and checking passwords."""

    def __init__(self):
        """Initialize a password manager instance."""
        self.context = CryptContext(
            schemes=['argon2'],
            deprecated='auto',
        )

    def hashpwd(self, password: str):
        """Hash the given password and return the hash as string."""
        return self.context.hash(password)

    def checkpwd(self, password: str, pwdhash: str):
        """Return true if the password results in the hash, else False."""
        return self.context.verify(password, pwdhash)


class TokenManager:
    """The TokenManager manages encoding and decoding JSON Web Tokens."""

    PRIVATE_KEY = open('jwtRS256.key').read()
    PUBLIC_KEY = open('jwtRS256.key.pub').read()

    ACCESS_TOKEN_TTL = os.getenv('ACCESS_TOKEN_TTL')
    REFRESH_TOKEN_TTL = os.getenv('REFRESH_TOKEN_TTL')

    def generate_token(self, user_id: str, ttl: int):
        payload = {
            'uid': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(ttl),
        }
        return jwt.encode(payload, self.PRIVATE_KEY, algorithms='RS256')

    def generate_access_token(self, user_id: str):
        return self.generate_token(user_id, self.ACCESS_TOKEN_TTL)

    def generate_refresh_token(self, user_id: str):
        return self.generate_token(user_id, self.REFRESH_TOKEN_TTL)

    def decode(self):
        raise NotImplementedError
        # except ExpiredSignatureError
