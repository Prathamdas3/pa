from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Tasks
from app.core import get_logger
from uuid import UUID

logger = get_logger(__name__)

class TaskRepo:
    def __init__(self,session:AsyncSession):
        self._db = session

    async def get_tasks_by_user_id(self,user_id:UUID):
        logger.debug(f"Repository: get tasks for user_id={user_id}")
        result = await self._db.execute(
            select(Tasks).where(Tasks.user_id == user_id, not Tasks.is_deleted )
        )
        tasks = result.scalars().all()
        logger.debug(f"Repository: found {len(tasks)} tasks")
        return tasks

    async def get_task_by_id(self,task_id:UUID,user_id:UUID):
        logger.debug(f"Repository: get task by id={task_id}, user_id={user_id}")
        result = await self._db.execute(
            select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id, not Tasks.is_deleted)
        )
        task = result.scalars().first()
        logger.debug(f"Repository: found task={task is not None}")
        return task

    async def save(self,task:Tasks):
        logger.debug(f"Repository: saving task id={task.id}")
        self._db.add(task)
        await self._db.commit()
        await self._db.refresh(task)
        logger.debug("Repository: task saved successfully")
        return task

    async def delete(self,task:Tasks):
        logger.debug(f"Repository: soft deleting task id={task.id}")
        task.is_deleted = True
        await self.save(task)
        logger.debug("Repository: task soft deleted")