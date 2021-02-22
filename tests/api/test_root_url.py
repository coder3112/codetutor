from fastapi.testclient import TestClient

from src import main

app = main.app
test_client = TestClient(app)


def test_root_url_status_code():
    response = test_client.get("/")
    assert response.status_code == 200


def test_root_url_content():
    response = test_client.get("/")
    assert response.json() == {"message": "Welcome to CodeTutor"}
