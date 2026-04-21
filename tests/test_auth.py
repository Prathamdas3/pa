import pytest
from httpx import AsyncClient


class TestUserRegistration:
    async def test_signup_user_success(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "newuser@test.com",
                "username": "newuser",
                "password": "NewUser@1234",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["email"] == "newuser@test.com"
        assert data["data"]["username"] == "newuser"
        assert "access_jwt" in response.cookies

    async def test_signup_admin_success(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/admin",
            json={
                "email": "newadmin@test.com",
                "username": "newadmin",
                "password": "NewAdmin@1234",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["email"] == "newadmin@test.com"
        assert data["data"]["username"] == "newadmin"

    async def test_signup_duplicate_email(self, test_client: AsyncClient, test_user):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": test_user["email"],
                "username": "anotheruser",
                "password": "Another@1234",
            },
        )
        assert response.status_code == 401

    async def test_signup_duplicate_username(self, test_client: AsyncClient, test_user):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "different@test.com",
                "username": test_user["username"],
                "password": "Another@1234",
            },
        )
        assert response.status_code == 401

    async def test_signup_weak_password(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "weakpass@test.com",
                "username": "weakpass",
                "password": "password",
            },
        )
        assert response.status_code == 422

    async def test_signup_password_no_uppercase(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "nopass@test.com",
                "username": "nopass",
                "password": "password@1234",
            },
        )
        assert response.status_code == 422

    async def test_signup_password_no_lowercase(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "nopass@test.com",
                "username": "nopass",
                "password": "PASSWORD@1234",
            },
        )
        assert response.status_code == 422

    async def test_signup_password_no_number(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "nopass@test.com",
                "username": "nopass",
                "password": "Password@",
            },
        )
        assert response.status_code == 422

    async def test_signup_password_no_special(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "nopass@test.com",
                "username": "nopass",
                "password": "Password1234",
            },
        )
        assert response.status_code == 422

    async def test_signup_reserved_username(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "admin@test.com",
                "username": "admin",
                "password": "Admin@1234",
            },
        )
        assert response.status_code == 422

    async def test_signup_reserved_username_root(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/sign-up/user",
            json={
                "email": "root@test.com",
                "username": "root",
                "password": "Root@1234",
            },
        )
        assert response.status_code == 422


class TestLogin:
    async def test_login_success(self, test_client: AsyncClient, test_user):
        response = await test_client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == test_user["email"]
        assert "access_jwt" in response.cookies

    async def test_login_wrong_password(self, test_client: AsyncClient, test_user):
        response = await test_client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user["email"],
                "password": "WrongPass@1234",
            },
        )
        assert response.status_code == 401

    async def test_login_nonexistent_email(self, test_client: AsyncClient):
        response = await test_client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@test.com",
                "password": "Test@1234",
            },
        )
        assert response.status_code == 401

    async def test_login_weak_password(self, test_client: AsyncClient, test_user):
        response = await test_client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user["email"],
                "password": "password",
            },
        )
        assert response.status_code == 422


class TestLogout:
    async def test_logout_success(self, test_client: AsyncClient, test_user, user_cookies):
        response = await test_client.post(
            "/api/v1/auth/logout",
            cookies=user_cookies,
        )
        assert response.status_code == 200
        assert "access_jwt" not in response.cookies or not response.cookies.get("access_jwt")

    async def test_logout_no_token(self, test_client: AsyncClient):
        response = await test_client.post("/api/v1/auth/logout")
        assert response.status_code == 401


class TestTokenRefresh:
    async def test_refresh_success(self, test_client: AsyncClient, user_cookies):
        response = await test_client.get(
            "/api/v1/auth/refresh",
            cookies=user_cookies,
        )
        assert response.status_code == 200

    async def test_refresh_no_token(self, test_client: AsyncClient):
        response = await test_client.get("/api/v1/auth/refresh")
        assert response.status_code == 401


class TestProtectedRoutes:
    async def test_access_protected_without_token(self, test_client: AsyncClient):
        response = await test_client.get("/api/v1/tasks/")
        assert response.status_code == 401

    async def test_access_protected_with_invalid_token(self, test_client: AsyncClient):
        response = await test_client.get(
            "/api/v1/tasks/",
            cookies={"access_jwt": "invalid_token"},
        )
        assert response.status_code == 401
