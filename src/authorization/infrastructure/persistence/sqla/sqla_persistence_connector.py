from functools import cached_property

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from authorization.application.exception.persistence import (
    PersistenceConnectionError,
)

logger = structlog.get_logger(__name__)


class SQLAPersistenceConnector:
    def __init__(
        self,
        dsn: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=dsn,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def connect(self) -> None:
        try:
            async with self._engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
            logger.info("db.connected", dsn=self._safe_dsn)
        except Exception as e:
            logger.error("db.connection_error", dsn=self._safe_dsn, error=str(e))
            raise PersistenceConnectionError(
                f"[{self._safe_dsn}] Connection error occurred: {e}."
            ) from e

    async def disconnect(self) -> None:
        await self._engine.dispose()
        logger.info("db.disconnected", dsn=self._safe_dsn)

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    @cached_property
    def _safe_dsn(self) -> str:
        return self._engine.url.render_as_string(hide_password=True)
