import pytest
from app.infrastructure.database.models.role_model import RoleModel

@pytest.fixture
def setup_roles(db):
    db.add(RoleModel(name="admin"))
    db.add(RoleModel(name="user"))
    db.add(RoleModel(name="guest"))
    db.commit()

def test_create_user_success(client, setup_roles):
    response = client.post("/users/", json={
        "name": "João Büttenbender",
        "email": "joao@email.com",
        "password": "Password123",
        "role_id": 1
    })
    assert response.status_code == 201
    assert response.json()["email"] == "joao@email.com"

def test_create_user_duplicate_email(client, setup_roles):
    client.post("/users/", json={
        "name": "João Büttenbender",
        "email": "joao@email.com",
        "password": "Password123",
        "role_id": 1
    })

    response = client.post("/users/", json={
        "name": "João Büttenbender",
        "email": "joao@email.com",
        "password": "Password123",
        "role_id": 1
    })
    assert response.status_code == 400

def test_create_user_invalid_password(client, setup_roles):
    response = client.post("/users/", json={
        "name": "João Büttenbender",
        "email": "joao@email.com",
        "password": "abc",
        "role_id": 1
    })
    assert response.status_code == 422

def test_get_user_requires_auth(client, setup_roles):
    response = client.get("/users/1")
    assert response.status_code == 401

def test_login_success(client, setup_roles):
    client.post("/users/", json={
        "name": "João Büttenbender",
        "email": "joao@email.com",
        "password": "Password123",
        "role_id": 1
    })

    response = client.post("/auth/login", json={
        "email": "joao@email.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, setup_roles):
    client.post("/users/", json={
        "name": "João Büttenbender",
        "email": "joao@email.com",
        "password": "Password123",
        "role_id": 1
    })

    response = client.post("/auth/login", json={
        "email": "joao@email.com",
        "password": "WrongPassword123"
    })
    assert response.status_code == 401