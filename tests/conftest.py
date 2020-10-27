
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
    assert(os.getenv("DB_CONNECTION_STRING") is not None)
    from pymongo import MongoClient
    client = MongoClient(os.getenv("DB_CONNECTION_STRING"))
    return client["testing"]['authentication']


def get_content_dict(response):
    assert(isinstance(response.content, bytes))
    content_string = response.content.decode()
    assert(isinstance(content_string, str))
    content_dict = json.loads(content_string)
    assert(isinstance(content_dict, dict))
    return content_dict


def assert_oauth2_token_response(content_dict):
    assert("oauth2_token" in content_dict)
    assert(all([key in content_dict["oauth2_token"] for key in
                ["access_token", "refresh_token", "token_type"]]))


def assert_account_response(content_dict):
    assert("account" in content_dict)
    assert(all([key in content_dict["account"] for key in
                ["email", "email_verified"]]))


def email_account(n: int):
    assert(n > 0)
    return f"test+{n}@fastsurvey.io"
