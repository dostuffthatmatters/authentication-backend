
import json
import os
import time
from dotenv import load_dotenv, find_dotenv
import pytest

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
os.environ["ENVIRONMENT"] = "testing"  # nopep8


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from app import app
    return TestClient(app)


@pytest.fixture(scope="module")
def account_collection():
    assert(os.getenv("MONGO_DB_CONNECTION_STRING") is not None)
    from pymongo import MongoClient
    client = MongoClient(os.getenv("MONGO_DB_CONNECTION_STRING"))
    return client["testing"]['authentication']


def get_content_dict(response):
    assert(isinstance(response.content, bytes))
    content_string = response.content.decode()
    assert(isinstance(content_string, str))
    content_dict = json.loads(content_string)
    assert(isinstance(content_dict, dict))
    return content_dict
