import os

from fastapi import FastAPI, Form
from motor.motor_asyncio import AsyncIOMotorClient

from app.account import AccountManager


# check that required environment variables are set
assert all([
    os.getenv(var)
    for var
    in [
        'ENVIRONMENT',
        'FRONTEND_URL',
        'AUTHENTICATION_URL',
        'MONGODB_CONNECTION_STRING',
        'MAILGUN_API_KEY',
        'ACCESS_TOKEN_TTL',
        'REFRESH_TOKEN_TTL',
        'SALT',
    ]
])

# check that public/private keypair is provided
assert 'jwtRS256.key' in os.listdir()
assert 'jwtRS256.key.pub' in os.listdir()

PRIVATE_KEY = open('jwtRS256.key').read()
PUBLIC_KEY = open('jwtRS256.key.pub').read()

# development / production / testing environment specification
ENVIRONMENT = os.getenv('ENVIRONMENT')
# MongoDB connection string
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')


# create fastapi app
app = FastAPI()
# connect to mongodb via pymongo and motor
motor_client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
# get link to development / production / testing database
database = motor_client[ENVIRONMENT]
# instantiate account manager
# TODO database used anywhere else? -> put database setup inside AccountManager
account_manager = AccountManager(database)


@app.get('/')
def status():
    return {
        'environment': ENVIRONMENT,
        'public_key': PUBLIC_KEY,
        'private_key': 'loljustkidding',
    }


@app.post('/registration')
async def create(
        email: str = Form(..., description='The primary account key'),
        password: str = Form(..., description='The account password'),
    ):
    await account_manager.create(email, password)
    return {'oauth2_token': 'TODO'}


@app.post('/verification')
async def verify(
        token: str = Form(..., description='The account verification token'),
        password: str = Form(..., description='The account password'),
    ):
    await account_manager.verify(token, password)
    return {'oauth2_token': 'TODO'}
