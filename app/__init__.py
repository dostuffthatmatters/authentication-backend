
import time
import os
import httpx
import certifi
import jwt
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

# Set correct SSL certificate
os.environ['SSL_CERT_FILE'] = certifi.where()

assert(all([
    isinstance(os.getenv(env_var), str) for env_var in [
        'ENVIRONMENT',
        'DB_CONNECTION_STRING',
        'PASSWORD_SALT',
        'HASH_ALGORITHM',
        'ACCESS_TOKEN_LIFETIME',
        'REFRESH_TOKEN_LIFETIME',
        'MAILGUN_API_KEY',
        'ADMIN_FRONTEND_URL',
        'AUTH_BACKEND_URL'
    ]
]))

assert(os.getenv('ENVIRONMENT') in ['production', 'development', 'testing'])
assert(os.getenv('ACCESS_TOKEN_LIFETIME').isnumeric)
assert(os.getenv('REFRESH_TOKEN_LIFETIME').isnumeric)

assert("jwtRS256.key" in os.listdir("."))
assert("jwtRS256.key.pub" in os.listdir("."))
PRIVATE_KEY = open('jwtRS256.key').read()
PUBLIC_KEY = open('jwtRS256.key.pub').read()

# Self Check
token = jwt.encode(
    {"some": "data"}, PRIVATE_KEY,
    algorithm=os.getenv("HASH_ALGORITHM")
)
plain = jwt.decode(
    token, PUBLIC_KEY,
    algorithms=os.getenv("HASH_ALGORITHM")
)
assert(plain == {"some": "data"})


# Set all environment variables
ENVIRONMENT = os.getenv('ENVIRONMENT')
ADMIN_FRONTEND_URL = os.getenv('ADMIN_FRONTEND_URL')
AUTH_BACKEND_URL = os.getenv('AUTH_BACKEND_URL')

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Using the synchronous MongoClient during setup for
# for index-creation and testing
pymongo_client = MongoClient(os.getenv('DB_CONNECTION_STRING'))
motor_client = AsyncIOMotorClient(os.getenv('DB_CONNECTION_STRING'))
database = motor_client[ENVIRONMENT]
account_collection = database['authentication']

if ENVIRONMENT == "testing":
    pymongo_client["testing"]['authentication'].delete_many({})
    # Dropping indexes to ensure create_index works as expected
    pymongo_client["testing"]['authentication'].drop_indexes()

# I really don't know why the index is called "email_1"
# instead of just "email"
db_indexes = pymongo_client[ENVIRONMENT]['authentication'].index_information()
if "email_1" not in db_indexes:
    print(f"db_indexes: {db_indexes}")
    print("Creating email uniqueness index")
    pymongo_client[ENVIRONMENT]['authentication'].create_index("email", unique=True)

# Getting rid of the unused client
del pymongo_client
del MongoClient

httpx_client = httpx.AsyncClient(
    auth=('api', os.getenv('MAILGUN_API_KEY')),
    base_url="https://api.eu.mailgun.net/v3/email.fastsurvey.io"
)

from app.routes import *  # nopep8
