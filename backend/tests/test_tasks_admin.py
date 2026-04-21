import pytest
from uuid import uuid4
from httpx import AsyncClient


class TestAdminTaskAccess:
    async def test_admin_get_all_tasks_success(self, test_client: AsyncClient, admin_cookies, test_user, user_cookies):
        await test_client.post(
            "/api/v1/tasks/",
            json={"title": "User Task"},
            cookies=user_cookies,
        )
        
        response = await test_client.get("/api/v1/tasks/admin/all", cookies=admin_cookies)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)

    async def test_regular_user_cannot_access_admin_tasks(self, test_client: AsyncClient, user_cookies):
        response = await test_client.get("/api/v1/tasks/admin/all", cookies=user_cookies)
        assert response.status_code == 403

    async def test_no_token_cannot_access_admin_tasks(self, test_client: AsyncClient):
        response = await test_client.get("/api/v1/tasks/admin/all")
        assert response.status_code == 401


class TestAdminTaskGetById:
    async def test_admin_get_task_by_id_success(self, test_client: AsyncClient, admin_cookies, user_cookies):
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.get(f"/api/v1/tasks/admin/{task_id}", cookies=admin_cookies)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Test Task"

    async def test_admin_get_nonexistent_task(self, test_client: AsyncClient, admin_cookies):
        fake_id = str(uuid4())
        response = await test_client.get(f"/api/v1/tasks/admin/{fake_id}", cookies=admin_cookies)
        assert response.status_code == 404


class TestAdminTaskDelete:
    async def test_admin_delete_task_success(self, test_client: AsyncClient, admin_cookies, user_cookies):
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.delete(f"/api/v1/tasks/admin/{task_id}", cookies=admin_cookies)
        assert response.status_code == 200

    async def test_admin_delete_nonexistent_task(self, test_client: AsyncClient, admin_cookies):
        fake_id = str(uuid4())
        response = await test_client.delete(f"/api/v1/tasks/admin/{fake_id}", cookies=admin_cookies)
        assert response.status_code == 404


class TestTaskUserIsolation:
    async def test_user_cannot_access_other_user_task(self, test_client: AsyncClient, user_cookies):
        await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Another User Task"},
            cookies=user_cookies,
        )
        
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.get(f"/api/v1/tasks/{task_id}", cookies=user_cookies)
        assert response.status_code == 200