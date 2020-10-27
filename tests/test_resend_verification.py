
from symbol import and_test

from tests.conftest import email_account, get_content_dict

INVALID_TEST_ACCOUNT = {"email": "70"}
VALID_TEST_ACCOUNT = {"email": email_account(70)}
REGISTERED_TEST_ACCOUNT = {"email": email_account(71), "password": "123456789"}


def resend_verification(client, data, status_code):
    response = client.post("/resend-verification", data=data)
    assert(response.status_code == status_code)


def test_resend_verification(client):
    resend_verification(client, INVALID_TEST_ACCOUNT, 200)
    resend_verification(client, VALID_TEST_ACCOUNT, 200)

    response = client.post("/register", data=REGISTERED_TEST_ACCOUNT)
    assert(response.status_code == 200)

    resend_verification(client, {"email": REGISTERED_TEST_ACCOUNT["email"]}, 200)
