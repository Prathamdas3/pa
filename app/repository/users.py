from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models import Users
from app.core import get_logger
from uuid import UUID

logger = get_logger(__name__)


class UserRepo:
    def __init__(self,session:AsyncSession):
        self._db = session

    async def get_user_by_email(self,email:str):
        logger.debug(f"Repository: get user by email={email}")
        result = await self._db.execute(
            select(Users).where(Users.email == email)
        )
        user = result.scalars().first()
        logger.debug(f"Repository: found user={user is not None}")
        return user

    async def get_user_by_id(self,user_id:UUID):
        logger.debug(f"Repository: get user by id={user_id}")
        result = await self._db.execute(
            select(Users).where(Users.id == user_id)
        )
        user = result.scalars().first()
        logger.debug(f"Repository: found user={user is not None}")
        return user

    async def save(self,user:Users):
        logger.debug(f"Repository: saving user id={user.id}")
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        logger.debug("Repository: user saved successfully")
        return user

    async def delete(self,user:Users):
        logger.debug(f"Repository: soft deleting user id={user.id}")
        user.is_active = False
        await self.save(user)
        logger.debug("Repository: user soft deleted")