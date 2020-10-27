
from tests.conftest import get_content_dict, email_account, \
    assert_jwt_account_response


TEST_ACCOUNT = {"email": email_account(50), "password": "000abcd!"}


def get_account(client, access_token, status_code):
    response = client.get("/account", headers={
        "Authorization": "bearer " + access_token
    })
    assert(response.status_code == status_code)


def test_refresh_token(client):
    # Login with not-registered account
    response = client.post("/login/form", data=TEST_ACCOUNT)
    assert(response.status_code == 401)

    # Registered that account
    response = client.post("/register", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Login with registered account
    response = client.post("/login/form", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Check whether response has the right format
    content_dict = get_content_dict(response)
    access_token_1 = content_dict["jwt"]["access_token"]
    refresh_token_1 = content_dict["jwt"]["refresh_token"]

    # Try to get private data with valid access_token
    get_account(client, access_token_1, 200)

    # Try to get private data with valid access_token
    response = client.post("/login/refresh", data={
        "refresh_token": refresh_token_1
    })
    assert(response.status_code == 200)
    content_dict = get_content_dict(response)
    assert_jwt_account_response(content_dict)
    access_token_2 = content_dict["jwt"]["access_token"]

    # Both access tokens work now!
    get_account(client, access_token_1, 200)
    get_account(client, access_token_2, 200)
