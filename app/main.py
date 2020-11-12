import os
import base64

from fastapi import FastAPI, Form, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.account import AccountManager
from app.cryptography import TokenManager


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
        'PUBLIC_RSA_KEY',
        'PRIVATE_RSA_KEY',
    ]
])


# decode public/private key pair
os.environ['PUBLIC_RSA_KEY'] = base64.b64decode(os.getenv('PUBLIC_RSA_KEY'))
os.environ['PRIVATE_RSA_KEY'] = base64.b64decode(os.getenv('PRIVATE_RSA_KEY'))


# development / production / testing environment specification
ENVIRONMENT = os.getenv('ENVIRONMENT')
# MongoDB connection string
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
# public JWT signature key
PUBLIC_RSA_KEY = os.getenv('PUBLIC_RSA_KEY')


# create fastapi app
app = FastAPI()
# connect to mongodb via pymongo and motor
motor_client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
# get link to development / production / testing database
database = motor_client[ENVIRONMENT]
# instantiate account manager
# TODO database used anywhere else? -> put database setup inside AccountManager
account_manager = AccountManager(database)
# instantiate token manager
token_manager = TokenManager(database)


@app.get('/')
def status():
    return {
        'environment': ENVIRONMENT,
        'public_rsa_key': PUBLIC_RSA_KEY,
    }


@app.post('/registration')
async def create(
        email: str = Form(..., description='The primary account key'),
        password: str = Form(..., description='The account password'),
    ):
    await account_manager.create(email, password)
    return {'oauth2_token': 'TODO'}


@app.post('/registration/resend-verification-email')
async def resend_verification_email():
    raise HTTPException(501, 'not implemented')


@app.post('/verification')
async def verify(
        token: str = Form(..., description='The account verification token'),
        password: str = Form(..., description='The account password'),
    ):
    await account_manager.verify(token, password)
    return {'oauth2_token': 'TODO'}


@app.post('/authentication/password')
async def authenticate_from_password():
    raise HTTPException(501, 'not implemented')


@app.post('/authentication/access-token')
async def authenticate_from_access_token():
    raise HTTPException(501, 'not implemented')


@app.post('/authentication/refresh-token')
async def authenticate_from_refresh_token():
    raise HTTPException(501, 'not implemented')


@app.post('/password/change')
async def change_password():
    raise HTTPException(501, 'not implemented')


@app.post('/password/request-reset')
async def request_password_reset():
    raise HTTPException(501, 'not implemented')


@app.post('/password/reset')
async def reset_password():
    raise HTTPException(501, 'not implemented')
