
import json
import os
os.environ["ENVIRONMENT"] = "testing"  # nopep8

from fastapi.testclient import TestClient
from app import app
import time


client = TestClient(app)


def test_environment():
    response = client.get("/")
    assert(response.status_code == 200)
    assert(isinstance(response.content, bytes))
    content_string = response.content.decode()
    assert(isinstance(content_string, str))
    content_dict = json.loads(content_string)
    assert(isinstance(content_dict, dict))
    assert(all([key in content_dict for key in ["status", "mode"]]))
    assert(content_dict["mode"] == "testing")


TEST_SET_1 = [
    {
        "data": {"email": "a", "password": "000000aa"},
        "result": False  # Invalid format
    }, {
        "data": {"email": "a", "password": "000000a!"},
        "result": True
    }, {
        "data": {"email": "a", "password": "000000b!"},
        "result": False  # Invalid format
    }, {
        "data": {"email": "b", "password": "000000c!"},
        "result": True
    }, {
        "data": {"email": "b", "password": "000000d!"},
        "result": False
    },
]


def test_registration():
    for test in TEST_SET_1:
        response = client.post("/register", data=test["data"])
        print(f"test: {test}, \nresponse: {response.content}\n")  # Only prints if test fails
        assert(response.status_code == (200 if test["result"] else 400))
        time.sleep(0.5)  # Account creation does not use atomic operations yet! Required!!!
