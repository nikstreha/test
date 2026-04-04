from sqlalchemy import select

from authorization.application.port.persistence.repository.user.reader import (
    IUserReader,
)
from authorization.application.query_model.user import UserQueryModel
from authorization.infrastructure.persistence.sqla.table.user import user_table
from authorization.infrastructure.persistence.sqla.type import ReaderSession


class SQLAUserReader(IUserReader):
    def __init__(self, session: ReaderSession) -> None:
        self._session = session

    async def read_by_id(self, *, user_id: int) -> UserQueryModel | None:
        stmt = select(
            user_table,
        ).where(user_table.c.id == user_id)

        response = await self._session.execute(stmt)
        row = response.mappings().one_or_none()

        if row:
            return UserQueryModel(**row)
        return None

    async def read_by_email(self, *, email: str) -> UserQueryModel | None:
        stmt = select(
            user_table,
        ).where(user_table.c.email == email)

        response = await self._session.execute(stmt)
        row = response.mappings().one_or_none()

        if row:
            return UserQueryModel(**row)
        return None
