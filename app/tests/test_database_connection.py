"""Simple database connection tests."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
@pytest.mark.database
class TestDatabaseConnection:
    """Test basic database connection functionality."""

    async def test_database_connection(self, test_db_session: AsyncSession):
        """Test that we can connect to the database."""
        result = await test_db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1
