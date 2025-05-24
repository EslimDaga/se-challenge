"""Unit tests for database session components."""

from unittest.mock import AsyncMock, patch
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, async_engine
from app.core.config import get_settings


@pytest.mark.unit
@pytest.mark.database
class TestDatabaseConfiguration:
    """Test database configuration."""

    def test_database_settings_loaded(self):
        """Test that database settings are properly loaded."""
        settings = get_settings()

        assert settings.database_url is not None
        assert "mysql+aiomysql://" in settings.database_url
        assert settings.mysql_host in settings.database_url

    def test_database_engine_configuration(self):
        """Test that database engine is properly configured."""
        assert async_engine is not None
        assert async_engine.url.drivername == "mysql+aiomysql"


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.database
class TestDatabaseSession:
    """Test database session management."""

    def test_get_db_generator(self):
        """Test that get_db returns a generator."""
        db_gen = get_db()
        assert hasattr(db_gen, "__iter__") or hasattr(db_gen, "__aiter__")

    @patch("app.db.session.async_session")
    async def test_get_db_session_lifecycle(self, mock_async_session):
        """Test database session lifecycle."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_async_session.return_value.__aenter__.return_value = mock_session
        mock_async_session.return_value.__aexit__.return_value = None

        db_gen = get_db()
        session = await db_gen.__anext__()

        assert session is not None
        mock_async_session.assert_called_once()
