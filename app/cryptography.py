from passlib.context import CryptContext


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
