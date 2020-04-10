import warnings

import schemas
from database import SessionLocal

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)


from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

sess = SessionLocal()

username = "admin"
password = "admin"
token_headers = {}

def test_logout_without_auth():
    response = client.get("/api/logout")
    assert response.status_code == 401
    #assert response.json() == dict(message="ok")


def test_login_missing_username():
    response = client.post("/api/login", json=dict(
        password=password
    ))
    assert response.status_code == 422


def test_login_missing_password():

    response = client.post("/api/login", json=dict(
        password=password
    ))
    assert response.status_code == 422


def test_login():

    response = client.post("/api/login", json=dict(
            username=username,
            password=password
        )
    )
    assert response.status_code == 200  # Must have status code 200
    assert "user" in response.json()
    assert "token_type" in response.json()
    assert "access_token" in response.json()
    token_headers["Authorization"] = response.json()["token_type"] + " " + response.json()["access_token"]
    return response


def test_logout_with_auth():
    response = client.get("/api/logout", headers=token_headers)
    assert response.status_code == 200


def test_user_edit():

    user = schemas.UserInDB(
        username="test",
        password="test",
        full_name="test",
        email="test",
        role="test"
    )

    user.sync(sess=sess)

    db_user = user.from_db(sess)
    #print(db_user.username)




