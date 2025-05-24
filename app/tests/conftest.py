"""Test configuration and fixtures."""

from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.sql import text
import aiomysql
from dotenv import load_dotenv
from loguru import logger

from app.core.config import get_settings


load_dotenv()

settings = get_settings()


test_engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

TestAsyncSession = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "database: Database tests")
    config.addinivalue_line("markers", "unit: Unit tests")


@pytest_asyncio.fixture(scope="function")
async def test_db_engine():
    """Create a test database engine."""
    yield test_engine


@pytest_asyncio.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for testing."""
    session = None
    try:
        session = TestAsyncSession()

        await session.execute(text("SELECT 1"))
        yield session
    except aiomysql.Error as e:
        logger.error(f"Failed to create test database session: {str(e)}")
        if session:
            await session.rollback()
        raise
    finally:
        if session:
            try:
                await session.rollback()
                await session.close()
            except aiomysql.Error as e:
                logger.warning(f"Error closing test session: {str(e)}")


@pytest_asyncio.fixture(scope="function")
async def mysql_raw_connection():
    """Create a raw MySQL connection for basic testing."""
    connection = None
    try:
        connection = await aiomysql.connect(
            host=settings.mysql_host,
            port=int(settings.mysql_port),
            user=settings.mysql_user,
            password=settings.mysql_password,
            db=settings.mysql_database,
            autocommit=False,
        )
        yield connection
    except Exception as e:
        logger.error(f"Failed to create raw MySQL connection: {str(e)}")
        raise
    finally:
        if connection:
            try:
                connection.close()
            except aiomysql.Error as e:
                logger.warning(f"Error closing raw connection: {str(e)}")


@pytest.fixture(scope="function")
def database_config():
    """Provide database configuration for tests."""
    return {
        "host": settings.mysql_host,
        "port": int(settings.mysql_port),
        "user": settings.mysql_user,
        "database": settings.mysql_database,
        "url": settings.database_url,
    }
