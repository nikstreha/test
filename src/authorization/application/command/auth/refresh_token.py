import structlog

from authorization.application.dto.auth import (
    UserRefreshTokenRequestDTO,
    UserRefreshTokenResponseDTO,
)
from authorization.application.exception.auth import InvalidCredentialError
from authorization.application.port.persistence.repository.user.reader import (
    IUserReader,
)
from authorization.application.port.security.token_provider import ITokenProvider

logger = structlog.get_logger(__name__)


class RefreshTokenInteractor:
    def __init__(
        self,
        token_provider: ITokenProvider,
        user_reader: IUserReader,
    ):
        self._token_provider = token_provider
        self._user_reader = user_reader

    async def __call__(
        self, request: UserRefreshTokenRequestDTO
    ) -> UserRefreshTokenResponseDTO:
        try:
            user_id = self._token_provider.get_user_id_from_token(
                token=request.refresh_token, token_type="refresh"
            )
        except Exception as e:
            logger.warning("token.refresh_invalid")
            raise InvalidCredentialError("Invalid or expired refresh token") from e

        user_qm = await self._user_reader.read_by_id(user_id=user_id.value)  # type: ignore
        if not user_qm or not user_qm.is_active:
            logger.warning("token.refresh_user_inactive", user_id=user_id.value)
            raise InvalidCredentialError("User not found or inactive")

        new_access_token = self._token_provider.create_access_token(
            user_id=user_id, role=user_qm.role
        )
        new_refresh_token = self._token_provider.create_refresh_token(
            user_id=user_id, role=user_qm.role
        )

        logger.info("token.refresh_success", user_id=user_id.value)

        return UserRefreshTokenResponseDTO(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
