import pytest  # type: ignore
from httpx import AsyncClient  # type: ignore
from main import app


@pytest.mark.asyncio(scope="module")
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Testpassword123@",
        }
        response = await client.post("/register/", json=user_data)
        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully"}


@pytest.mark.asyncio(scope="module")
async def test_register_existing_user():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        user_data = {
            "username": "hp-AGM",
            "email": "user@example.com",
            "password": "Favourboydddddd1998",
        }
        response = await client.post("/register/", json=user_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already exists"


@pytest.mark.asyncio(scope="module")
async def test_login_valid_credentials():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        user_data = {"email": "user@example.com", "password": "User1234@"}
        response = await client.post("/login/", json=user_data)
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio(scope="module")
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        user_data = {"email": "test@example.com", "password": "wrongpassword"}
        response = await client.post("/login/", json=user_data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"
