"""Integration tests for user API endpoints."""

import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
class TestUserAPIGetUsers:
    """Test cases for GET /api/v1/users endpoint."""

    async def test_get_users(self) -> None:
        """Test retrieving users from the API."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.get(
                "/api/v1/users/", params={"page": 1, "size": 10}
            )
            assert response.status_code == 200


@pytest.mark.asyncio
class TestUserAPIPostUser:
    """Test cases for POST /api/v1/users endpoint."""

    async def test_post_user(self) -> None:
        """Test creating a new user via the API."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.post(
                "/api/v1/users/",
                json={
                    "username": "testuser",
                    "email": "testuser@gmail.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "role": "user",
                    "active": True,
                },
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 201


@pytest.mark.asyncio
class TestUserAPIGetUserById:
    """Test cases for GET /api/v1/users/{user_id} endpoint."""

    async def test_get_user_by_id(self) -> None:
        """Test retrieving a user by ID from the API."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.get("/api/v1/users/1")
            assert response.status_code == 200


@pytest.mark.asyncio
class TestUserAPIUpdateUser:
    """Test cases for PUT /api/v1/users/{user_id} endpoint."""

    async def test_update_user(self) -> None:
        """Test updating an existing user via the API."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.put(
                "/api/v1/users/1",
                json={
                    "first_name": "Updated",
                    "last_name": "User",
                    "email": "userupdated@mail.com",
                    "role": "admin",
                    "active": False,
                },
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200


@pytest.mark.asyncio
class TestUserAPIDeleteUser:
    """Test cases for DELETE /api/v1/users/{user_id} endpoint."""

    async def test_delete_user(self) -> None:
        """Test deleting a user via the API."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.delete("/api/v1/users/1")
            assert response.status_code == 204


@pytest.mark.asyncio
class TestUserAPIHardDeleteUser:
    """Test cases for hard delete user endpoint."""

    async def test_hard_delete_user(self) -> None:
        """Test hard deleting a user via the API."""
        async with AsyncClient(base_url="http://localhost:8000") as client:
            response = await client.delete("/api/v1/users/1/hard")
            assert response.status_code == 204
