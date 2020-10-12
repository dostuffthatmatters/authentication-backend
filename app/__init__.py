
import time
import os

from fastapi import FastAPI
from app.setup import *
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

motor_client = AsyncIOMotorClient(MONGO_DB_CONNECTION_STRING)
database = motor_client[ENVIRONMENT]
account_collection = database['authentication']

if ENVIRONMENT == "testing":
    # Using the synchronous pymongo library because I
    # want to keep the test synchronous as well. No real
    # advantage from having asynchronous test just more
    # complexity - for now ...
    from pymongo import MongoClient
    client = MongoClient(MONGO_DB_CONNECTION_STRING)
    client["testing"]['authentication'].delete_many({})

from app.routes import *  # nopep8
