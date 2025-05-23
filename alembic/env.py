import os
import asyncio
from dotenv import load_dotenv
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.db.base import Base
from app.models.user import User

load_dotenv()

config = context.config

section = config.config_ini_section
config.set_section_option(section, "MYSQL_USER", os.environ.get("MYSQL_USER"))
config.set_section_option(section, "MYSQL_PASSWORD", os.environ.get("MYSQL_PASSWORD"))
config.set_section_option(section, "MYSQL_HOST", os.environ.get("MYSQL_HOST"))
config.set_section_option(section, "MYSQL_PORT", os.environ.get("MYSQL_PORT"))
config.set_section_option(section, "MYSQL_DATABASE", os.environ.get("MYSQL_DATABASE"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
