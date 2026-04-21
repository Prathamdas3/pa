from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import AsyncGenerator, Annotated
from app.core.config import config
from app.core.logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

logger = get_logger(__name__)

class AsyncDatabase:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_async_engine(
            self.url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=10,
            max_overflow=20,
        )
        self._session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database session error, rolled back: {e}", exc_info=True)
                raise
            finally:
                await session.close()
            

db = AsyncDatabase(url=config.database_url)
logger.info(f"Database initialized: PostgreSQL at {db.url}")

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db.session():
        yield session  
                
                
SessionDep = Annotated[AsyncSession, Depends(get_session)]