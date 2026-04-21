from app.repository import TaskRepo
from app.core import AppException
from app.models import Tasks
from app.schemas import TaskCreate, TaskUpdate
from uuid import UUID


class TaskService:
    """Service class for managing tasks."""

    def __init__(self, repo: TaskRepo):
        self._repo = repo

    async def get_tasks_by_user_id(self, user_id: str):
        """Get all tasks for a user."""
        return await self._repo.get_tasks_by_user_id(user_id)

    async def get_task_by_id(self, task_id: str, user_id: str):
        """Get a specific task by id for a user."""
        task = await self._repo.get_task_by_id(task_id, user_id)
        if not task:
            raise AppException("Task not found.", status_code=404)
        return task

    async def create_task(self, data: TaskCreate, user_id: UUID):
        """Create a new task for a user."""
        task = Tasks(**data.model_dump(), user_id=user_id)
        return await self._repo.save(task)

    async def update_task(self, task_id: str, data: TaskUpdate, user_id: str):
        """Update an existing task for a user."""
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            raise AppException("Task not found.", status_code=404)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        return await self._repo.save(task)

    async def delete_task(self, task_id: str, user_id: str):
        """Soft delete a task for a user."""
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            raise AppException("Task not found.", status_code=404)
        await self._repo.delete(task)
