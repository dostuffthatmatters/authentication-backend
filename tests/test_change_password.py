
from tests.conftest import get_content_dict, TEST_EMAIL_DOMAIN


TEST_ACCOUNT = {"email": "e" + TEST_EMAIL_DOMAIN, "password": "123456a!"}
MODIFIED_TEST_ACCOUNT = {"email": "e" + TEST_EMAIL_DOMAIN, "password": "123456a!!!"}


def account(account_collection):
    return account_collection.find_one(
        {"email": TEST_ACCOUNT["email"]}
    )


def test_login(client, account_collection):
    # Login with not-registered account
    response = client.post("/login", data=TEST_ACCOUNT)
    assert(response.status_code == 401)

    # Registered that account
    response = client.post("/register", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Login with registered account
    response = client.post("/login", data=TEST_ACCOUNT)
    assert(response.status_code == 200)
    access_token = get_content_dict(response)["access_token"]

    account_in_db = account(account_collection)
    assert(account_in_db["email_verified"] == False)

    client.post("/verify", data={
        "email_token": account_in_db["email_token"],
        "password": TEST_ACCOUNT["password"]
    })

    account_in_db = account(account_collection)
    assert(account_in_db["email_verified"] == True)
