from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models import Users


class UserRepo:
    def __init__(self,session:AsyncSession):
        self._db = session
        
    async def get_user_by_email(self,email:str):
        result = await self._db.execute(
            select(Users).where(Users.email == email)
        )
        return result.scalars().first()
    
    async def get_user_by_id(self,user_id:str):
        result = await self._db.execute(
            select(Users).where(Users.id == user_id)
        )
        return result.scalars().first()

    async def save(self,user:Users):
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user
    
    async def delete(self,user:Users):
        user.is_active = False
        await self.save(user)