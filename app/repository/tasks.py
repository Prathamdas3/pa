from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Tasks

class TaskRepo:
    def __init__(self,session:AsyncSession):
        self._db = session
    
    async def get_tasks_by_user_id(self,user_id:str):
        result = await self._db.execute(
            select(Tasks).where(Tasks.user_id == user_id, not Tasks.is_deleted )
        )
        return result.scalars().all()
    
    async def get_task_by_id(self,task_id:str,user_id:str):
        result = await self._db.execute(
            select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id, not Tasks.is_deleted)
        )
        return result.scalars().first()
    
    async def save(self,task:Tasks):
        self._db.add(task)
        await self._db.commit()
        await self._db.refresh(task)
        return task
    
    async def delete(self,task:Tasks):
        task.is_deleted = True
        await self.save(task)