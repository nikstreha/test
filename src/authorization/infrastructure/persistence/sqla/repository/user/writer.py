from sqlalchemy import select

from authorization.application.port.persistence.repository.user.writer import (
    IUserWriter,
)
from authorization.domain.entity.user import User
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.id import UserId
from authorization.infrastructure.persistence.sqla.type import WriterSession


class SQLAUserWriter(IUserWriter):
    def __init__(self, session: WriterSession) -> None:
        self._session = session

    async def add(self, *, user: User) -> None:
        self._session.add(user)

    async def find_by_id(
        self, *, user_id: UserId, for_update: bool = False
    ) -> User | None:
        stmt = select(User).where(User._id == user_id)  # type: ignore[attr-defined]

        if for_update:
            stmt = stmt.with_for_update()

        response = await self._session.execute(stmt)
        return response.scalars().one_or_none()

    async def find_by_email(self, *, email: UserEmail) -> User | None:
        stmt = select(User).where(User.email == email)  # type: ignore[attr-defined]
        response = await self._session.execute(stmt)
        return response.scalars().one_or_none()
