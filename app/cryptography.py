from passlib.context import CryptContext


class PasswordManager:
    """The PasswordManager manages hashing and checking passwords."""

    def __init__(self):
        """Initialize a password manager instance."""
        self.context = CryptContext(
            schemes=['argon2'],
            deprecated='auto',
        )

    def hash(self, password: str):
        """Hash the given password and return the hash as string."""
        return self.context.hash(password)

    def verify(self, password: str, hash: str):
        """Return true if the password results in the hash, else False."""
        return self.context.verify(password, hash)
