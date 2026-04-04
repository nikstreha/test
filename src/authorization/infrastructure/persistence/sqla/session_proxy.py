from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from authorization.infrastructure.persistence.sqla.sqla_uow import SQLAUnitOfWork


class SessionProxy:
    def __init__(self, uow: SQLAUnitOfWork) -> None:
        object.__setattr__(self, "_uow", uow)

    def _get_real_session(self) -> AsyncSession:
        if (session := self._uow._session) is None:
            raise RuntimeError(
                "Session is not available. Ensure you are within an 'async with uow:' block."
            )
        return session

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get_real_session(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self._get_real_session(), name, value)

    def __delattr__(self, name: str) -> None:
        delattr(self._get_real_session(), name)
