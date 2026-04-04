import structlog

from authorization.application.dto.auth import (
    TokensResponseDTO,
    UserSignInRequestDTO,
    UserSignInResponseDTO,
)
from authorization.application.dto.user import UserResponseDTO
from authorization.application.exception.auth import InvalidCredentialError
from authorization.application.port.persistence.repository.audit_log.writer import (
    IAuditLogWriter,
)
from authorization.application.port.persistence.repository.user.writer import (
    IUserWriter,
)
from authorization.application.port.persistence.uow import IUnitOfWork
from authorization.application.port.security.token_provider import ITokenProvider
from authorization.domain.enum.audit.event import AuditEvent
from authorization.domain.service.user.authentication import UserAuthenticationService
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.raw_password import RawPassword

logger = structlog.get_logger(__name__)


class SignInInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        user_writer: IUserWriter,
        audit_log_writer: IAuditLogWriter,
        user_authentication_service: UserAuthenticationService,
        token_provider: ITokenProvider,
    ):
        self._uow = uow
        self._user_writer = user_writer
        self._audit_log_writer = audit_log_writer
        self._user_authentication_service = user_authentication_service
        self._token_provider = token_provider

    async def __call__(self, request: UserSignInRequestDTO) -> UserSignInResponseDTO:
        email = UserEmail(request.email)
        password = RawPassword(request.password)

        async with self._uow:
            user = await self._user_writer.find_by_email(email=email)

            if not user:
                logger.warning("login.user_not_found", email=request.email)
                raise InvalidCredentialError("Invalid email or password")

            is_authenticated = await self._user_authentication_service.authenticate(
                user=user, raw_password=password
            )

            if not is_authenticated:
                logger.warning("login.invalid_password", email=request.email)
                raise InvalidCredentialError("Invalid email or password.")

            await self._audit_log_writer.add(
                user_id=user.id_.value,
                event=AuditEvent.LOGIN,
                ip=request.ip,
            )

        access_token = self._token_provider.create_access_token(
            user_id=user.id_, role=user.role
        )
        refresh_token = self._token_provider.create_refresh_token(
            user_id=user.id_, role=user.role
        )

        logger.info("login.success", email=request.email, user_id=user.id_.value)

        return UserSignInResponseDTO(
            tokens=TokensResponseDTO(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
            user=UserResponseDTO(
                id=user.id_.value, # type: ignore
                email=user.email.value,
                full_name=user.full_name.value if user.full_name else None,
                phone=user.phone.value if user.phone else None,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )
