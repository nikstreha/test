from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from authorization.application.port.persistence.uow import IUnitOfWork


class SQLAUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._session:
            try:
                if exc_type:
                    await self._rollback()
                else:
                    await self._commit()
            finally:
                await self._session.close()
                self._session = None

    async def _commit(self) -> None:
        if self._session:
            await self._session.commit()

    async def _rollback(self) -> None:
        if self._session:
            await self._session.rollback()

    async def flush(self) -> None:
        if self._session:
            await self._session.flush()
