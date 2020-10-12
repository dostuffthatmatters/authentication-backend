
import time
import os

from fastapi import FastAPI
from app.setup import *
from passlib.context import CryptContext
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Using the synchronous MongoClient during setup for
# for index-creation and testing
client = MongoClient(MONGO_DB_CONNECTION_STRING)
motor_client = AsyncIOMotorClient(MONGO_DB_CONNECTION_STRING)
database = motor_client[ENVIRONMENT]
account_collection = database['authentication']

if ENVIRONMENT == "testing":
    client["testing"]['authentication'].delete_many({})
    # Dropping indexes to ensure create_index works as expected
    client["testing"]['authentication'].drop_indexes()

# I really don't know why the index is called "email_1"
# instead of just "email"
db_indexes = client["testing"]['authentication'].index_information()
if "email_1" not in db_indexes:
    print(f"db_indexes: {db_indexes}")
    print("Creating email uniqueness index")
    client[ENVIRONMENT]['authentication'].create_index("email", unique=True)

# Getting rid of the unused client
del client
del MongoClient

from app.routes import *  # nopep8
