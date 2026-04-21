from app.repository import TaskRepo
from app.core import AppException, get_logger
from app.models import Tasks
from app.schemas import TaskCreate, TaskUpdate
from uuid import UUID

logger = get_logger(__name__)


class TaskService:
    """Service class for managing tasks."""

    def __init__(self, repo: TaskRepo):
        self._repo = repo

    async def get_tasks_by_user_id(self, user_id: UUID):
        """Get all tasks for a user."""
        logger.debug(f"Getting tasks for user_id={user_id}")
        tasks = await self._repo.get_tasks_by_user_id(user_id)
        logger.debug(f"Retrieved {len(tasks)} tasks for user_id={user_id}")
        return tasks

    async def get_task_by_id(self, task_id: UUID, user_id: UUID):
        """Get a specific task by id for a user."""
        logger.debug(f"Getting task: task_id={task_id}, user_id={user_id}")
        task = await self._repo.get_task_by_id(task_id, user_id)
        if not task:
            logger.warning(f"Task not found: task_id={task_id}")
            raise AppException("Task not found.", status_code=404)
        return task

    async def create_task(self, data: TaskCreate, user_id: UUID):
        """Create a new task for a user."""
        logger.debug(f"Creating task: title={data.title}, user_id={user_id}")
        task = Tasks(**data.model_dump(), user_id=user_id)
        result = await self._repo.save(task)
        logger.info(f"Task created: id={result.id}")
        return result

    async def update_task(self, task_id: UUID, data: TaskUpdate, user_id: UUID):
        """Update an existing task for a user."""
        logger.debug(f"Updating task: task_id={task_id}, user_id={user_id}")
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            logger.warning(f"Task update failed: task not found, task_id={task_id}")
            raise AppException("Task not found.", status_code=404)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        result = await self._repo.save(task)
        logger.info(f"Task updated: id={task_id}")
        return result

    async def delete_task(self, task_id: UUID, user_id: UUID):
        """Soft delete a task for a user."""
        logger.debug(f"Deleting task: task_id={task_id}, user_id={user_id}")
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            logger.warning(f"Task deletion failed: task not found, task_id={task_id}")
            raise AppException("Task not found.", status_code=404)
        await self._repo.delete(task)
        logger.info(f"Task deleted: id={task_id}")

    async def get_all_tasks(self):
        """Get all tasks (admin)."""
        logger.debug("Getting all tasks (admin)")
        tasks = await self._repo.get_all_tasks()
        logger.debug(f"Retrieved {len(tasks)} tasks")
        return tasks

    async def get_task_by_id_admin(self, task_id: UUID):
        """Get any task by id (admin)."""
        logger.debug(f"Getting task (admin): task_id={task_id}")
        task = await self._repo.get_task_by_id_no_user(task_id)
        if not task:
            logger.warning(f"Task not found: task_id={task_id}")
            raise AppException("Task not found.", status_code=404)
        return task

    async def delete_task_admin(self, task_id: UUID):
        """Delete any task (admin)."""
        logger.debug(f"Deleting task (admin): task_id={task_id}")
        task = await self._repo.get_task_by_id_no_user(task_id)
        if not task:
            logger.warning(f"Task deletion failed: task not found, task_id={task_id}")
            raise AppException("Task not found.", status_code=404)
        await self._repo.delete(task)
        logger.info(f"Task deleted by admin: id={task_id}")
