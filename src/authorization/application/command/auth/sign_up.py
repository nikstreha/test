import structlog

from authorization.application.dto.auth import (
    TokensResponseDTO,
    UserSignUpRequestDTO,
    UserSignUpResponseDTO,
)
from authorization.application.dto.user import UserResponseDTO
from authorization.application.exception.auth import UserAlreadyExistError
from authorization.application.port.persistence.repository.audit_log.writer import (
    IAuditLogWriter,
)
from authorization.application.port.persistence.repository.user.writer import (
    IUserWriter,
)
from authorization.application.port.persistence.uow import IUnitOfWork
from authorization.application.port.security.token_provider import ITokenProvider
from authorization.domain.enum.audit.event import AuditEvent
from authorization.domain.service.user.registration import UserRegistrationService
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.full_name import FullUserName
from authorization.domain.value_object.user.phone import UserPhone
from authorization.domain.value_object.user.raw_password import RawPassword

logger = structlog.get_logger(__name__)


class SignUpInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        user_writer: IUserWriter,
        audit_log_writer: IAuditLogWriter,
        user_registration_service: UserRegistrationService,
        token_provider: ITokenProvider,
    ):
        self._uow = uow
        self._user_writer = user_writer
        self._audit_log_writer = audit_log_writer
        self._user_registration_service = user_registration_service
        self._token_provider = token_provider

    async def __call__(self, request: UserSignUpRequestDTO) -> UserSignUpResponseDTO:
        email = UserEmail(request.email)
        password = RawPassword(request.password)
        full_name = FullUserName(request.full_name) if request.full_name else None
        phone = UserPhone(request.phone) if request.phone else None

        async with self._uow:
            if await self._user_writer.find_by_email(email=email):
                logger.warning("registration.duplicate_email", email=request.email)
                raise UserAlreadyExistError("User with this email already exist.")

            user = await self._user_registration_service.register(
                email=email,
                password=password,
                full_name=full_name,
                phone=phone,
            )

            await self._user_writer.add(user=user)
            await self._uow.flush()
            await self._audit_log_writer.add(
                user_id=user.id_.value,  # type: ignore
                event=AuditEvent.REGISTER,
                ip=request.ip,
            )

        access_token = self._token_provider.create_access_token(
            user_id=user.id_, role=user.role
        )
        refresh_token = self._token_provider.create_refresh_token(
            user_id=user.id_, role=user.role
        )

        logger.info("registration.success", email=request.email, user_id=user.id_.value)

        return UserSignUpResponseDTO(
            tokens=TokensResponseDTO(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
            user=UserResponseDTO(
                id=user.id_.value,  # type: ignore
                email=user.email.value,
                full_name=user.full_name.value if user.full_name else None,
                phone=user.phone.value if user.phone else None,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )
