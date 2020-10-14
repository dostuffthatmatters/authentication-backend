
from app.utilities.encryption import validate_password_format

TEST_SET = [
    {"password": "abc", "result": False},
    {"password": "abcabcab", "result": False},
    {"password": "12312312", "result": False},
    {"password": "!?!?!?!?", "result": False},
    {"password": "abc123ab", "result": False},
    {"password": "abc!?!ab", "result": False},
    {"password": "123!?!12", "result": False},
    {"password": "000000a!", "result": True},
    {"password": "sdasds8!sdasds8!sdasds8!sdasds8!", "result": True},
    {"password": "sdasds8!sdasds8!sdasds8!sdasds8!a", "result": False}
]


def test_password_format():
    for test in TEST_SET:
        assert(validate_password_format(test["password"]) == test["result"])
