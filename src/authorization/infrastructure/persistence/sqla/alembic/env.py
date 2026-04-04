import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

root_path = Path(__file__).resolve().parents[5]
sys.path.append(str(root_path))

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from authorization.composition.configuration.settings import Settings
from authorization.infrastructure.persistence.sqla.mapper.all import map_table
from authorization.infrastructure.persistence.sqla.registry import mapping_registry

SRC_PATH = Path(__file__).parent.parent.parent.parent.parent.parent.resolve()

if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

configuration: Settings = Settings()  # type: ignore

config = context.config

config.set_main_option("sqlalchemy.url", configuration.postgres_dsn)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

map_table()
target_metadata = mapping_registry.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    db_url = config.get_main_option("sqlalchemy.url")
    if not db_url:
        raise ValueError("Database URL must be set for Alembic migrations.")

    connectable = create_async_engine(
        db_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
