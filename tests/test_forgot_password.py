
from symbol import and_test

from tests.conftest import TEST_EMAIL_DOMAIN, get_content_dict

TEST_ACCOUNT = {"email": "f" + TEST_EMAIL_DOMAIN, "password": "123456a!"}
MODIFIED_TEST_ACCOUNT = {"email": "f" + TEST_EMAIL_DOMAIN, "password": "123456a!!!"}


def login(client, data, status_code):
    response = client.post("/login", data=data)
    assert(response.status_code == status_code)
    if status_code == 200:
        return get_content_dict(response)["access_token"]


def restore_forgotten_password(
    client, forgot_password_token, new_password, status_code
):
    response = client.post("/restore-forgotten-password", data={
        "forgot_password_token": forgot_password_token,
        "new_password": new_password,
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

    response = client.post("/forgot-password", data={
        "email": TEST_ACCOUNT["email"]
    })
    assert(response.status_code == 200)

    # Login with current account still works
    login(client, TEST_ACCOUNT, 200)

    forgot_password_token = account(account_collection)["forgot_password_token"]

    for test in [
        {
            "forgot_password_token": "123",
            "new_password": "123",
            "status_code": 400
        }, {
            "forgot_password_token": "123",
            "new_password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 400
        }, {
            "forgot_password_token": forgot_password_token,
            "new_password": "123",
            "status_code": 400
        }, {
            "forgot_password_token": forgot_password_token,
            "new_password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 200
        }
    ]:
        restore_forgotten_password(client, **test)

    login(client, TEST_ACCOUNT, 401)
    login(client, MODIFIED_TEST_ACCOUNT, 200)

    assert("forgot_password_token" not in account(account_collection))
