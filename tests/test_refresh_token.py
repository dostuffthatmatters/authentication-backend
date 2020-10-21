
from tests.conftest import get_content_dict, TEST_EMAIL_DOMAIN


TEST_ACCOUNT = {"email": "g" + TEST_EMAIL_DOMAIN, "password": "000abcd!"}


def test_refresh_token(client):
    # Login with not-registered account
    response = client.post("/login", data=TEST_ACCOUNT)
    assert(response.status_code == 401)

    # Registered that account
    response = client.post("/register", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Login with registered account
    response = client.post("/login", data=TEST_ACCOUNT)
    assert(response.status_code == 200)

    # Check whether response has the right format
    content_dict = get_content_dict(response)
    assert(all([key in content_dict for key in [
        "access_token", "refresh_token", "token_type"]
    ]))
    access_token_1 = content_dict["access_token"]
    refresh_token_1 = content_dict["refresh_token"]

    # Try to get private data with valid access_token
    response = client.get("/account", headers={
        "Authorization": "bearer " + access_token_1
    })
    assert(response.status_code == 200)

    # Try to get private data with valid access_token
    response = client.post("/refresh", data={
        "refresh_token": refresh_token_1
    })
    assert(response.status_code == 200)
    content_dict = get_content_dict(response)
    assert(all([key in content_dict for key in [
        "access_token", "refresh_token", "token_type"]
    ]))
    access_token_2 = content_dict["access_token"]

    # Both access tokens work now!
    response = client.get("/account", headers={
        "Authorization": "bearer " + access_token_1
    })
    assert(response.status_code == 200)
    response = client.get("/account", headers={
        "Authorization": "bearer " + access_token_2
    })
    assert(response.status_code == 200)
