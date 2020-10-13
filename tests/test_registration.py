
import json
import os
import time
from tests.conftest import TEST_EMAIL_DOMAIN

TEST_SET_1 = [
    {
        "data": {"email": "a", "password": "000000aa"},
        "result": False  # Invalid emailformat
    }, {
        "data": {"email": "a" + TEST_EMAIL_DOMAIN, "password": "000000aa"},
        "result": False  # Invalid password format
    }, {
        "data": {"email": "a" + TEST_EMAIL_DOMAIN, "password": "000000a!"},
        "result": True
    }, {
        "data": {"email": "a" + TEST_EMAIL_DOMAIN, "password": "000000b!"},
        "result": False  # Email already taken
    }, {
        "data": {"email": "b" + TEST_EMAIL_DOMAIN, "password": "000000c!"},
        "result": True
    }, {
        "data": {"email": "b" + TEST_EMAIL_DOMAIN, "password": "000000d!"},
        "result": False
    },
]


def test_registration(client):
    for test in TEST_SET_1:
        response = client.post("/register", data=test["data"])
        print(f"test: {test}, \nresponse: {response.content}\n")  # Only prints if test fails
        assert(response.status_code == (200 if test["result"] else 400))
        time.sleep(0.1)  # Account creation does not use atomic operations yet! Required!!!
