
import os

from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv

import certifi
import os


# Set correct SSL certificate
os.environ['SSL_CERT_FILE'] = certifi.where()


# Initialize environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

assert os.getenv('ENV') in ['PRODUCTION', 'DEVELOPMENT']
assert os.getenv('MONGO_DB_CONNECTION_STRING') != None

IN_PRODUCTION = (os.getenv('ENV') == 'PRODUCTION')
MONGO_DB_CONNECTION_STRING = os.getenv('MONGO_DB_CONNECTION_STRING')


app = FastAPI()


@app.get('/')
def index():
    return 'Hello FastAPI', 200
