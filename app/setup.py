
from dotenv import load_dotenv, find_dotenv

import certifi
import os


# Set correct SSL certificate
os.environ['SSL_CERT_FILE'] = certifi.where()


# Initialize environment variables
ENVIRONMENT = os.getenv('ENVIRONMENT')
assert(ENVIRONMENT in [None, "testing"])

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

assert(all([
    isinstance(os.getenv(env_var), str) for env_var in [
        'ENVIRONMENT', 'MONGO_DB_CONNECTION_STRING', 'PASSWORD_SALT',
        'SECRET_KEY', 'HASH_ALGORITHM', 'ACCESS_TOKEN_EXPIRE_MINUTES'
    ]
]))
assert(os.getenv('ENVIRONMENT') in ['production', 'development', 'testing'])
assert(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES').isnumeric)

MONGO_DB_CONNECTION_STRING = os.getenv('MONGO_DB_CONNECTION_STRING')
PASSWORD_SALT = os.getenv('PASSWORD_SALT')
SECRET_KEY = os.getenv('SECRET_KEY')
HASH_ALGORITHM = os.getenv('HASH_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

os.getenv('ENVIRONMENT') if ENVIRONMENT is None else ENVIRONMENT
