
import json
import os
os.environ["ENVIRONMENT"] = "testing"  # nopep8

from fastapi.testclient import TestClient
from app import app


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
