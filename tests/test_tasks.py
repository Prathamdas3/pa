import pytest
from uuid import uuid4
from httpx import AsyncClient
from datetime import datetime, timedelta, timezone


class TestTaskCreate:
    async def test_create_task_success(self, test_client: AsyncClient, user_cookies):
        response = await test_client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Test description",
                "priority": "high",
                "status": "pending",
            },
            cookies=user_cookies,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["title"] == "Test Task"

    async def test_create_task_title_too_short(self, test_client: AsyncClient, user_cookies):
        response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "AB"},
            cookies=user_cookies,
        )
        assert response.status_code == 422

    async def test_create_task_title_too_long(self, test_client: AsyncClient, user_cookies):
        response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "A" * 101},
            cookies=user_cookies,
        )
        assert response.status_code == 422

    async def test_create_task_title_blank(self, test_client: AsyncClient, user_cookies):
        response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "   "},
            cookies=user_cookies,
        )
        assert response.status_code == 422

    async def test_create_task_no_title(self, test_client: AsyncClient, user_cookies):
        response = await test_client.post(
            "/api/v1/tasks/",
            json={"description": "Test"},
            cookies=user_cookies,
        )
        assert response.status_code == 422


class TestTaskGet:
    async def test_get_own_tasks(self, test_client: AsyncClient, user_cookies):
        await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        response = await test_client.get("/api/v1/tasks/", cookies=user_cookies)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)

    async def test_get_task_by_id(self, test_client: AsyncClient, user_cookies):
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.get(f"/api/v1/tasks/{task_id}", cookies=user_cookies)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Test Task"

    async def test_get_task_invalid_uuid(self, test_client: AsyncClient, user_cookies):
        response = await test_client.get("/api/v1/tasks/not-a-uuid", cookies=user_cookies)
        assert response.status_code == 422

    async def test_get_nonexistent_task(self, test_client: AsyncClient, user_cookies):
        fake_id = str(uuid4())
        response = await test_client.get(f"/api/v1/tasks/{fake_id}", cookies=user_cookies)
        assert response.status_code == 404


class TestTaskUpdate:
    async def test_update_task_success(self, test_client: AsyncClient, user_cookies):
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Original Title"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.patch(
            f"/api/v1/tasks/{task_id}",
            json={"title": "Updated Title"},
            cookies=user_cookies,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Updated Title"

    async def test_update_task_empty_fields(self, test_client: AsyncClient, user_cookies):
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.patch(
            f"/api/v1/tasks/{task_id}",
            json={},
            cookies=user_cookies,
        )
        assert response.status_code == 422

    async def test_update_nonexistent_task(self, test_client: AsyncClient, user_cookies):
        fake_id = str(uuid4())
        response = await test_client.patch(
            f"/api/v1/tasks/{fake_id}",
            json={"title": "Updated"},
            cookies=user_cookies,
        )
        assert response.status_code == 404


class TestTaskDelete:
    async def test_delete_task_success(self, test_client: AsyncClient, user_cookies):
        create_response = await test_client.post(
            "/api/v1/tasks/",
            json={"title": "Test Task"},
            cookies=user_cookies,
        )
        task_id = create_response.json()["data"]["id"]
        
        response = await test_client.delete(f"/api/v1/tasks/{task_id}", cookies=user_cookies)
        assert response.status_code == 200

    async def test_delete_nonexistent_task(self, test_client: AsyncClient, user_cookies):
        fake_id = str(uuid4())
        response = await test_client.delete(f"/api/v1/tasks/{fake_id}", cookies=user_cookies)
        assert response.status_code == 404
