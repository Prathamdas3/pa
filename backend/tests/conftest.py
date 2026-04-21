import os

os.environ["ENV"] = "testing"
os.environ["DEBUG"] = "true"
os.environ["DATABASE_URL"] = "postgresql+psycopg://myuser:mypassword@localhost:5433/testdb"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

import pytest
import asyncio
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, Dict, Any
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import jwt
from sqlmodel import SQLModel

from app.main import app
from app.core.db import get_session
from app.models import Users, Tasks


TEST_USER = {
    "email": "user@test.com",
    "username": "testuser",
    "password": "Test@1234",
}

TEST_ADMIN = {
    "email": "admin@test.com",
    "username": "testadmin",
    "password": "Admin@1234",
}


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(
        "postgresql+psycopg://myuser:mypassword@localhost:5433/testdb",
        echo=False,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=10,
        max_overflow=20,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def test_client(test_session) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


def create_test_token(user_id: str, role: str) -> str:
    from app.core.config import config
    from app.utils.jwt import create_access_token
    payload = {
        "sub": {
            "id": user_id,
            "email": f"{role}@test.com",
            "username": f"test{role}",
            "role": role,
        }
    }
    return create_access_token(payload)


@pytest.fixture(scope="function")
async def test_user(test_session: AsyncSession) -> Dict[str, Any]:
    from app.utils import hash_password

    user = Users(
        id=uuid4(),
        email=TEST_USER["email"],
        username=TEST_USER["username"],
        hashed_password=hash_password(TEST_USER["password"]),
        role="user",
        is_active=True,
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "password": TEST_USER["password"],
        "role": user.role,
    }


@pytest.fixture(scope="function")
async def test_admin(test_session: AsyncSession) -> Dict[str, Any]:
    from app.utils import hash_password

    admin = Users(
        id=uuid4(),
        email=TEST_ADMIN["email"],
        username=TEST_ADMIN["username"],
        hashed_password=hash_password(TEST_ADMIN["password"]),
        role="admin",
        is_active=True,
    )
    test_session.add(admin)
    await test_session.commit()
    await test_session.refresh(admin)
    return {
        "id": str(admin.id),
        "email": admin.email,
        "username": admin.username,
        "password": TEST_ADMIN["password"],
        "role": admin.role,
    }


@pytest.fixture(scope="function")
def user_token(test_user) -> str:
    return create_test_token(test_user["id"], "user")


@pytest.fixture(scope="function")
def admin_token(test_admin) -> str:
    return create_test_token(test_admin["id"], "admin")


@pytest.fixture(scope="function")
def user_cookies(user_token) -> Dict[str, str]:
    return {"access_jwt": user_token}


@pytest.fixture(scope="function")
def admin_cookies(admin_token) -> Dict[str, str]:
    return {"access_jwt": admin_token}