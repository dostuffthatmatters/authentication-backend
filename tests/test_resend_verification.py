
from symbol import and_test

from tests.conftest import TEST_EMAIL_DOMAIN, get_content_dict

INVALID_TEST_ACCOUNT = {"email": "h"}
VALID_TEST_ACCOUNT = {"email": "h" + TEST_EMAIL_DOMAIN}
REGISTERED_TEST_ACCOUNT = {"email": "i" + TEST_EMAIL_DOMAIN, "password": "123456789"}


def resend_verification(client, data, status_code):
    response = client.post("/resend-verification", data=data)
    assert(response.status_code == status_code)


def test_resend_verification(client):
    resend_verification(client, INVALID_TEST_ACCOUNT, 200)
    resend_verification(client, VALID_TEST_ACCOUNT, 200)

    response = client.post("/register", data=REGISTERED_TEST_ACCOUNT)
    assert(response.status_code == 200)

    resend_verification(client, {"email": REGISTERED_TEST_ACCOUNT["email"]}, 200)
