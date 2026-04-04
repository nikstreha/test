from authorization.application.dto.user import (
    UpdateUserDataRequestDTO,
    UserResponseDTO,
)
from authorization.application.exception.user import UserNotFound
from authorization.application.port.persistence.repository.user.reader import (
    IUserReader,
)
from authorization.application.port.persistence.repository.user.writer import (
    IUserWriter,
)
from authorization.application.port.persistence.uow import IUnitOfWork
from authorization.domain.value_object.user.full_name import FullUserName
from authorization.domain.value_object.user.id import UserId
from authorization.domain.value_object.user.phone import UserPhone


class UpdateUserDataInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        user_writer: IUserWriter,
        user_reader: IUserReader,
    ):
        self._uow = uow
        self._user_writer = user_writer
        self._user_reader = user_reader

    async def __call__(self, request: UpdateUserDataRequestDTO) -> UserResponseDTO:
        user_id = UserId(request.user_id)
        async with self._uow:
            user = await self._user_writer.find_by_id(user_id=user_id, for_update=True)

            if not user:
                raise UserNotFound("User not found")

            if request.phone is not None:
                user.phone = UserPhone(request.phone) if request.phone else None

            if request.full_name is not None:
                user.full_name = (
                    FullUserName(request.full_name) if request.full_name else None
                )

        updated_user_qm = await self._user_reader.read_by_id(
            user_id=request.user_id
        )

        if not updated_user_qm:
            raise UserNotFound("User not found")

        return UserResponseDTO(
            id=updated_user_qm.id,
            email=updated_user_qm.email,
            full_name=updated_user_qm.full_name,
            phone=updated_user_qm.phone,
            role=updated_user_qm.role,
            is_active=updated_user_qm.is_active,
            created_at=updated_user_qm.created_at,
        )
