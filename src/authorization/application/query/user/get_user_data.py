from authorization.application.exception.user import UserNotFound
from authorization.application.port.persistence.repository.user.reader import (
    IUserReader,
)
from authorization.application.query_model.user import UserQueryModel


class GetUserDataInteractor:
    def __init__(self, user_reader: IUserReader):
        self._user_reader = user_reader

    async def __call__(self, user_id: int) -> UserQueryModel:
        user_qm = await self._user_reader.read_by_id(user_id=user_id)

        if not user_qm:
            raise UserNotFound("User not found")

        return user_qm
