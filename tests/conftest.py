import asyncio
import subprocess

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.base import Base
from app.main import create_app

# Test database URL (use PostgreSQL for testing)
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Apply migrations before tests and rollback after."""
    subprocess.run(["uv", "run", "alembic", "upgrade", "head"], check=True)
    yield
    subprocess.run(["uv", "run", "alembic", "downgrade", "base"], check=True)


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create test database session."""
    TestSessionLocal = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def test_settings():
    """Create test settings."""
    return Settings(
        SECRET_KEY="test-secret-key-32-chars-long-here",
        DEBUG=True,
    )


@pytest.fixture
async def test_app(test_session, test_settings):
    """Create test FastAPI application."""
    app = create_app()

    # Override dependencies
    from app.core.deps import get_db, get_settings_dependency

    async def override_get_db():
        yield test_session

    def override_get_settings():
        return test_settings

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings_dependency] = override_get_settings

    yield app

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
async def client(test_app):
    """Create test HTTP client."""
    from httpx import ASGITransport

    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://testserver") as ac:
        yield ac
