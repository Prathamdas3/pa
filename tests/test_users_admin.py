import pytest
from uuid import uuid4
from httpx import AsyncClient


class TestAdminUserAccess:
    async def test_admin_get_all_users_success(self, test_client: AsyncClient, admin_cookies, test_user):
        response = await test_client.get("/api/v1/users/admin/all", cookies=admin_cookies)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    async def test_regular_user_cannot_access_admin_users(self, test_client: AsyncClient, user_cookies):
        response = await test_client.get("/api/v1/users/admin/all", cookies=user_cookies)
        assert response.status_code == 403

    async def test_no_token_cannot_access_admin_users(self, test_client: AsyncClient):
        response = await test_client.get("/api/v1/users/admin/all")
        assert response.status_code == 401


class TestAdminUserGetById:
    async def test_admin_get_user_by_id_success(self, test_client: AsyncClient, admin_cookies, test_user):
        response = await test_client.get(
            f"/api/v1/users/admin/{test_user['id']}",
            cookies=admin_cookies,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == test_user["id"]

    async def test_admin_get_nonexistent_user(self, test_client: AsyncClient, admin_cookies):
        fake_id = str(uuid4())
        response = await test_client.get(f"/api/v1/users/admin/{fake_id}", cookies=admin_cookies)
        assert response.status_code == 404


class TestAdminUserDelete:
    async def test_admin_delete_user_success(self, test_client: AsyncClient, admin_cookies, test_user):
        response = await test_client.delete(
            f"/api/v1/users/admin/{test_user['id']}",
            cookies=admin_cookies,
        )
        assert response.status_code == 200

    async def test_admin_delete_nonexistent_user(self, test_client: AsyncClient, admin_cookies):
        fake_id = str(uuid4())
        response = await test_client.delete(f"/api/v1/users/admin/{fake_id}", cookies=admin_cookies)
        assert response.status_code == 404


class TestAdminUserUpdateRole:
    async def test_admin_update_role_success(self, test_client: AsyncClient, admin_cookies, test_user):
        response = await test_client.patch(
            f"/api/v1/users/admin/{test_user['id']}/role",
            params={"role": "admin"},
            cookies=admin_cookies,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["role"] == "admin"

    async def test_admin_update_role_nonexistent_user(self, test_client: AsyncClient, admin_cookies):
        fake_id = str(uuid4())
        response = await test_client.patch(
            f"/api/v1/users/admin/{fake_id}/role",
            params={"role": "admin"},
            cookies=admin_cookies,
        )
        assert response.status_code == 404


class TestAdminUserRestore:
    async def test_admin_restore_deleted_user(self, test_client: AsyncClient, admin_cookies, test_session):
        from app.models import Users
        from app.utils import hash_password
        from uuid import UUID

        deleted_user = Users(
            id=uuid4(),
            email="restore@test.com",
            username="restoreuser",
            hashed_password=hash_password("Restore@1234"),
            role="user",
            is_active=False,
        )
        test_session.add(deleted_user)
        await test_session.commit()
        
        response = await test_client.patch(
            f"/api/v1/users/admin/{deleted_user.id}/restore",
            cookies=admin_cookies,
        )
        assert response.status_code == 200

    async def test_admin_restore_nonexistent_user(self, test_client: AsyncClient, admin_cookies):
        fake_id = str(uuid4())
        response = await test_client.patch(
            f"/api/v1/users/admin/{fake_id}/restore",
            cookies=admin_cookies,
        )
        assert response.status_code == 404


class TestAdminUserEdgeCases:
    async def test_regular_user_cannot_access_admin_user_by_id(self, test_client: AsyncClient, user_cookies, test_admin):
        response = await test_client.get(
            f"/api/v1/users/admin/{test_admin['id']}",
            cookies=user_cookies,
        )
        assert response.status_code == 403

    async def test_regular_user_cannot_delete_admin_user(self, test_client: AsyncClient, user_cookies, test_admin):
        response = await test_client.delete(
            f"/api/v1/users/admin/{test_admin['id']}",
            cookies=user_cookies,
        )
        assert response.status_code == 403

    async def test_regular_user_cannot_update_role(self, test_client: AsyncClient, user_cookies, test_user):
        response = await test_client.patch(
            f"/api/v1/users/admin/{test_user['id']}/role",
            params={"role": "admin"},
            cookies=user_cookies,
        )
        assert response.status_code == 403