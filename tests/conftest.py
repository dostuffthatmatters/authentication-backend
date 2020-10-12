
import pytest
import json
import os
import time

os.environ["ENVIRONMENT"] = "testing"  # nopep8


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from app import app
    return TestClient(app)
