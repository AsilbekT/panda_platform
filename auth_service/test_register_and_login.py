from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_new_user():
    response = client.post("/auth/register", json={"username": "testuser", "phone_number": "1234567890", "password": "password123"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "User created successfully", "data": {"username": "testuser"}}

def test_register_existing_username():
    client.post("/auth/register", json={"username": "testuser", "phone_number": "1234567890", "password": "password123"})  # First registration
    response = client.post("/auth/register", json={"username": "testuser", "phone_number": "0987654321", "password": "password456"})
    assert response.status_code == 400
    assert response.json() == {"status": "error", "message": "User already exists", "data": None}

def test_login_valid_credentials():
    client.post("/auth/register", json={"username": "testuser", "phone_number": "1234567890", "password": "password123"})  # Registration
    response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Login successful", "data": {"access_token": response.json()["data"]["access_token"], "token_type": "bearer"}}

def test_login_invalid_password():
    client.post("/auth/register", json={"username": "testuser", "phone_number": "1234567890", "password": "password123"})  # Registration
    response = client.post("/auth/login", json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json() == {"status": "error", "message": "Invalid credentials", "data": None}
