
from app.utilities.encryption import validate_password_format

TEST_SET = [
    {"password": "abc", "result": False},
    {"password": "sdasds8!sdasds8!sdasds8!sdasds8!", "result": True},
    {"password": "sdasds8!sdasds8!sdasds8!sdasds8!a", "result": False}
]


def test_password_format():
    for test in TEST_SET:
        assert(validate_password_format(test["password"]) == test["result"])
