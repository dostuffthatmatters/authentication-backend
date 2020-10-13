
from tests.conftest import get_content_dict, TEST_EMAIL_DOMAIN

TEST_ACCOUNT = {"email": "d" + TEST_EMAIL_DOMAIN, "password": "000000fg!"}


def verify_response(client, email_token, password):
    return client.post("/verify", data={
        "email_token": email_token,
        "password": password
    })


def account(account_collection):
    return account_collection.find_one(
        {"email": TEST_ACCOUNT["email"]}
    )


def test_verification(client, account_collection):
    response = client.post("/register", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    account_in_db = account(account_collection)
    assert(account_in_db is not None)
    assert(account_in_db["email_verified"] == False)

    # Submit incorrect password
    response = verify_response(
        client, account_in_db["email_token"], "123"
    )
    assert(response.status_code == 400)
    assert(account(account_collection)["email_verified"] == False)

    # Submit incorrect token
    response = verify_response(
        client, "123", TEST_ACCOUNT["password"]
    )
    assert(response.status_code == 400)
    assert(account(account_collection)["email_verified"] == False)

    # Submit correct token and password
    response = verify_response(
        client, account_in_db["email_token"], TEST_ACCOUNT["password"]
    )
    assert(response.status_code == 200)
    assert(account(account_collection)["email_verified"] == True)
