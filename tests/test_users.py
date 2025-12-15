"""
User endpoint tests
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation"""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "strongpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    """Test getting all users"""
    # Create a user first
    await client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )

    # Get users
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_duplicate_email(client: AsyncClient):
    """Test duplicate email validation"""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "password123"
    }

    # Create first user
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201

    # Try to create with same email
    user_data["username"] = "user2"
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400