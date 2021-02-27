import string

from src.schemas.user import UserOut
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from hypothesis import given, strategies as st, settings, Verbosity
from src import main

app = main.app
test_client = TestClient(app)


def test_token_url_correct():
    data = {"username": "admin", "password": "adminisgr8"}
    response = test_client.post(url="/token", data=data).json()
    assert response.get("access_token") != None
    assert response.get("user").get("active") == True
    assert response.get("user").get("admin") == True
    assert UserOut(**response.get("user"))


@given(
    wrongusername=st.text(min_size=1, alphabet=string.printable),
    wrongpassword=st.text(min_size=1, alphabet=string.printable),
)
@settings(max_examples=10, verbosity=Verbosity.verbose, deadline=None)
def test_token_url_wrong(wrongusername, wrongpassword):
    data = {"username": wrongusername, "password": wrongpassword}
    response = test_client.post(url="/token", data=data).json()
    assert response.get("access_token") == None
    assert response.get("detail") == "Could not validate credentials"
