
from symbol import and_test

from tests.conftest import email_account, get_content_dict

TEST_ACCOUNT = {"email": email_account(10), "password": "123456a!"}
MODIFIED_TEST_ACCOUNT = {"email": email_account(10), "password": "123456a!!!"}


def login(client, data, status_code):
    response = client.post("/login/form", data=data)
    assert(response.status_code == status_code)
    if status_code == 200:
        return get_content_dict(response)["jwt"]["access_token"]


def change_password(
    client, access_token, old_password, new_password, status_code
):
    response = client.post("/change-password", data={
        "old_password": old_password,
        "new_password": new_password,
    }, headers={"Authorization": "Bearer " + access_token})
    assert(response.status_code == status_code)


def account(account_collection):
    return account_collection.find_one(
        {"email": TEST_ACCOUNT["email"]}
    )


def test_change_password(client, account_collection):
    # Login with not-registered account
    login(client, TEST_ACCOUNT, 401)

    # Registered that account
    response = client.post("/register", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Login with registered account
    access_token = login(client, TEST_ACCOUNT, 200)

    assert(account(account_collection)["email_verified"] == False)

    for test in [
        {
            # access_token invalid
            "access_token": "123",
            "old_password": "123",
            "new_password": "123",
            "status_code": 401
        }, {
            # email not verified
            "access_token": access_token,
            "old_password": "123",
            "new_password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 401
        }
    ]:
        change_password(client, **test)

    account_in_db = account(account_collection)
    assert(account_in_db["email_verified"] == False)
    client.post("/verify", data={
        "email_token": account_in_db["email_token"],
        "password": TEST_ACCOUNT["password"]
    })
    assert(account(account_collection)["email_verified"] == True)

    for test in [
        {
            "old_password": "123",
            "new_password": "123",
            "status_code": 400
        }, {
            "old_password": "123",
            "new_password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 401
        }, {
            "old_password": TEST_ACCOUNT["password"],
            "new_password": MODIFIED_TEST_ACCOUNT["password"],
            "status_code": 200
        }
    ]:
        change_password(client, access_token, **test)

    login(client, TEST_ACCOUNT, 401)
    login(client, MODIFIED_TEST_ACCOUNT, 200)
