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


@app.post('/account/register')
async def register(
        email: str = Form(..., description='The primary account key'),
        password: str = Form(..., description='The account password'),
    ):
    await account_manager.create(email, password)
    return {'oauth2_token': 'TODO'}


@app.post('/account/resend-verification-email')
async def resend_verification_email():
    raise HTTPException(501, 'not implemented')


@app.post('/account/verify-email-address')
async def verify_email_address(
        token: str = Form(..., description='The account verification token'),
        password: str = Form(..., description='The account password'),
    ):
    await account_manager.verify(token, password)
    return {'oauth2_token': 'TODO'}


@app.post('/authentication/password')
async def authenticate_from_password():
    raise HTTPException(501, 'not implemented')


@app.post('/authentication/token')
async def authenticate_from_token(token: str = Form(...)):
    """Authenticate a user from an access or refresh JSON web token."""
    uid = token_manager.decode(token)
    return await account_manager.fetch(uid)


@app.post('/password/change')
async def change_password():
    raise HTTPException(501, 'not implemented')


@app.post('/password/request-reset')
async def request_password_reset():
    raise HTTPException(501, 'not implemented')


@app.post('/password/set-new-with-reset-token')
async def set_new_password():
    raise HTTPException(501, 'not implemented')
