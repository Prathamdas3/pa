import pytest
from uuid import uuid4
from httpx import AsyncClient


class TestUserMe:
    async def test_get_current_user(self, test_client: AsyncClient, user_cookies):
        response = await test_client.get("/api/v1/users/me", cookies=user_cookies)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data["data"]
        assert "email" in data["data"]

    async def test_get_current_user_no_token(self, test_client: AsyncClient):
        response = await test_client.get("/api/v1/users/me")
        assert response.status_code == 401


class TestUserUpdate:
    async def test_update_username_success(self, test_client: AsyncClient, user_cookies):
        response = await test_client.patch(
            "/api/v1/users/me",
            json={"username": "updateduser"},
            cookies=user_cookies,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["username"] == "updateduser"

    async def test_update_username_with_reserved_word(self, test_client: AsyncClient, user_cookies):
        response = await test_client.patch(
            "/api/v1/users/me",
            json={"username": "admin"},
            cookies=user_cookies,
        )
        assert response.status_code == 422

    async def test_update_username_already_taken(self, test_client: AsyncClient, test_user, user_cookies):
        await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "other@test.com",
                "username": "otheruser",
                "password": "Other@1234",
            },
        )
        response = await test_client.patch(
            "/api/v1/users/me",
            json={"username": "otheruser"},
            cookies=user_cookies,
        )
        assert response.status_code == 401


class TestUserDelete:
    async def test_delete_current_user(self, test_client: AsyncClient, user_cookies):
        response = await test_client.delete("/api/v1/users/me", cookies=user_cookies)
        assert response.status_code == 200

    async def test_delete_current_user_no_token(self, test_client: AsyncClient):
        response = await test_client.delete("/api/v1/users/me")
        assert response.status_code == 401


class TestUserAfterDelete:
    async def test_cannot_access_after_deletion(self, test_client: AsyncClient, user_cookies):
        await test_client.delete("/api/v1/users/me", cookies=user_cookies)
        
        response = await test_client.get("/api/v1/users/me", cookies=user_cookies)
        assert response.status_code == 401