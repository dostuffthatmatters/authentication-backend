
import json
import os
import time
from tests.conftest import email_account

TEST_SET_1 = [
    {
        "data": {"email": "60", "password": "000000a!"},
        "result": False  # Invalid email format
    }, {
        "data": {"email": email_account(60), "password": "000000"},
        "result": False  # Invalid password format
    }, {
        "data": {"email": email_account(60), "password": "000000a!"},
        "result": True
    }, {
        "data": {"email": email_account(60), "password": "000000b!"},
        "result": False  # Email already taken
    }, {
        "data": {"email": email_account(61), "password": "000000c!"},
        "result": True
    }, {
        "data": {"email": email_account(61), "password": "000000d!"},
        "result": False  # Email already taken
    },
]


def test_registration(client):
    for test in TEST_SET_1:
        response = client.post("/register", data=test["data"])
        print(f"test: {test}, \nresponse: {response.content}\n")  # Only prints if test fails
        assert(response.status_code == (200 if test["result"] else 400))
        time.sleep(0.1)  # Account creation does not use atomic operations yet! Required!!!
