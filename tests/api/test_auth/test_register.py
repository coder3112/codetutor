import string

from src.schemas.user import UserOut
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from hypothesis import given, strategies as st, settings, Verbosity
from src import main

app = main.app
test_client = TestClient(app)


def test_register_endpoint():
    data = {
        "username": "user2",
        "password": "userpass",
        "email": "user2@user.com",
        "first_name": "user",
        "last_name": "user",
    }
    response = test_client.post(url="/register", json=data)
    assert response.status_code == 201


def test_register_endpoint_username_not_unique():
    data = {
        "username": "admin",
        "password": "adminisgr8",
        "email": "email@email.com",
        "first_name": "admin",
        "last_name": "admin",
    }
    response = test_client.post(url="/register", json=data)
    assert response.status_code == 400


def test_register_endpoint_email_not_unique():
    data = {
        "username": "someusername",
        "password": "adminisgr8",
        "email": "admin@admin.com",
        "first_name": "admin",
        "last_name": "admin",
    }
    response = test_client.post(url="/register", json=data)
    assert response.status_code == 400
