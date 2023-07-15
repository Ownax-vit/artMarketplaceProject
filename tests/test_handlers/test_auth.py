import pytest
from fastapi.testclient import TestClient
from fastapi import status
from tests.conftest import fake


@pytest.fixture(scope="function")
def test_user() -> dict:
    user_data = {
        "email": fake.free_email(),
        "password": fake.password(length=40, special_chars=False, upper_case=False),
        "login": fake.user_name(),
    }
    return user_data


@pytest.fixture(scope="function")
def test_user_admin() -> dict:
    user_data = {
        "email": fake.free_email(),
        "password": fake.password(length=40, special_chars=False, upper_case=False),
        "login": fake.user_name(),
        "is_admin": True
    }
    return user_data


@pytest.mark.smoke
def test_create_user(client: TestClient, test_user: dict):
    resp = client.post("/auth/sign-up", json=test_user)
    assert resp.status_code == status.HTTP_201_CREATED
    res_data = resp.json()
    assert res_data["login"] == test_user["login"]
    assert res_data["email"] == test_user["email"]


@pytest.mark.xfail
def test_create_user_admin(client: TestClient, test_user_admin: dict):
    resp = client.post("/auth/sign-up", json=test_user_admin)
    assert resp.status_code == status.HTTP_201_CREATED
    res_data = resp.json()
    assert res_data["login"] == test_user_admin["login"]
    assert res_data["email"] == test_user_admin["email"]


@pytest.mark.parametrize(
    "data, status_code",
    (
        (
            {"email": fake.free_email(), "password": fake.password(length=40, special_chars=False, upper_case=False),
             "login": fake.user_name()},
            status.HTTP_201_CREATED,
        ),
        (
                {"email": fake.free_email(),
                 "password": fake.password(length=40, special_chars=False, upper_case=False),
                 "login": fake.user_name()},
                status.HTTP_201_CREATED,
        ),
        (
                {"email": fake.free_email(),
                 "password": fake.password(length=40, special_chars=False, upper_case=False),
                 "login": fake.user_name()},
                status.HTTP_201_CREATED,
        ),
    ),
)
@pytest.mark.smoke
def test_create_user_admin(client: TestClient, data: dict, status_code: int):
    resp = client.post("/auth/sign-up", json=data)
    assert resp.status_code == status_code
    res_data = resp.json()
    assert res_data["login"] == data["login"]
    assert res_data["email"] == data["email"]


@pytest.mark.smoke
def test_sign_in(client: TestClient, test_user: dict):
    resp = client.post("/auth/sign-up", json=test_user)
    assert resp.status_code == status.HTTP_201_CREATED
    res_data = resp.json()
    assert res_data["login"] == test_user["login"]
    assert res_data["email"] == test_user["email"]

    # test sign-in by email
    data_for_login = {"email": test_user["email"], "password": test_user["password"] }
    resp = client.post("/auth/sign-in", json=data_for_login)
    assert resp.status_code == status.HTTP_200_OK
    res_data_login = resp.json()
    assert res_data_login["login"] == res_data["login"]
    assert res_data_login["email"] == res_data["email"]
    assert res_data_login["id"] == res_data["id"]

    # test sign-in by login
    data_for_login = {"login": test_user["login"], "password": test_user["password"] }
    resp = client.post("/auth/sign-in", json=data_for_login)
    assert resp.status_code == status.HTTP_200_OK
    res_data_login = resp.json()
    assert res_data_login["login"] == res_data["login"]
    assert res_data_login["email"] == res_data["email"]
    assert res_data_login["id"] == res_data["id"]


# @pytest.mark.smoke
# def test_refresh(client: TestClient, test_user: dict):
#     resp = client.post("/auth/sign-up", json=test_user)
#     assert resp.status_code == status.HTTP_201_CREATED
#     res_data = resp.json()
#     assert res_data["login"] == test_user["login"]
#     assert res_data["email"] == test_user["email"]
#
#     key = settings.jwt_refresh_token_name,
#     value = f"{settings.jwt_token_prefix} {res_data['token']}",
#     cookies = httpx.Cookies()
#     cookies.set(key, value)
#
#     resp = client.post("/auth/refresh", cookies=cookies)
#     assert resp.status_code == status.HTTP_200_OK
#     res_data_login = resp.json()
#     assert res_data_login["login"] == res_data["login"]
#     assert res_data_login["email"] == res_data["email"]
#     assert res_data_login["id"] == res_data["id"]
#     assert res_data_login["token"] != res_data["token"]
# TODO разобраться с cookies - не устанавливаются
