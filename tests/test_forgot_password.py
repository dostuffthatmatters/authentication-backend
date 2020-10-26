
from symbol import and_test

from tests.conftest import TEST_EMAIL_DOMAIN, get_content_dict

TEST_ACCOUNT = {"email": "f" + TEST_EMAIL_DOMAIN, "password": "123456a!"}
MODIFIED_TEST_ACCOUNT = {"email": "f" + TEST_EMAIL_DOMAIN, "password": "123456a!!!"}


def login(client, data, status_code):
    response = client.post("/login/form", data=data)
    assert(response.status_code == status_code)


def restore_forgotten_password(
    client, password_token, password, status_code
):
    response = client.post("/set-new-password", data={
        "password_token": password_token,
        "password": password,
    })
    assert(response.status_code == status_code)


def account(account_collection):
    return account_collection.find_one(
        {"email": TEST_ACCOUNT["email"]}
    )


def test_login(client, account_collection):
    # Login with not-registered account
    login(client, TEST_ACCOUNT, 401)

    # Registered that account
    response = client.post("/register", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Login with registered account
    login(client, TEST_ACCOUNT, 200)

    response = client.post("/request-new-password", data={
        "email": TEST_ACCOUNT["email"]
    })
    assert(response.status_code == 200)

    # Login with current account still works
    login(client, TEST_ACCOUNT, 200)

    password_token = account(account_collection)["password_token"]

    for test in [
        {
            "password_token": "123",
            "password": "123",
            "status_code": 400
        }, {
            "password_token": "123",
            "password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 401
        }, {
            "password_token": password_token,
            "password": "123",
            "status_code": 400
        }, {
            "password_token": password_token,
            "password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 200
        }
    ]:
        restore_forgotten_password(client, **test)

    login(client, TEST_ACCOUNT, 401)
    login(client, MODIFIED_TEST_ACCOUNT, 200)

    db_account = account(account_collection)
    print("--> account", db_account)
    assert("password_token" not in db_account)
