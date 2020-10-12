
from tests.conftest import get_content_dict

TEST_ACCOUNT_1 = {"email": "c", "password": "000000d!"}
TEST_ACCOUNT_2 = {"email": "c", "password": "000000a!"}


def test_login(client):
    response = client.post("/register", data=TEST_ACCOUNT_2)
    assert(response.status_code == 200)

    response = client.post("/login", data=TEST_ACCOUNT_1)
    assert(response.status_code == 401)

    response = client.post("/login", data=TEST_ACCOUNT_2)
    assert(response.status_code == 200)

    content_dict = get_content_dict(response)
    assert(all([key in content_dict for key in ["access_token", "token_type"]]))
    assert(64 < len(content_dict["access_token"]) < 256)
    assert(content_dict["token_type"] == "bearer")

    response = client.post("/account", data={
        "access_token": "123"
    })
    assert(response.status_code == 401)

    response = client.post("/account", data={
        "access_token": content_dict["access_token"]
    })
    assert(response.status_code == 200)
    content_dict = get_content_dict(response)
    assert(content_dict == {"email": "c", "email_verified": False})
