from datetime import UTC, datetime, timedelta

import jwt

from authorization.application.exception.auth import InvalidTokenError
from authorization.application.port.security.token_provider import (
    ITokenProvider,
    TokenType,
)
from authorization.domain.enum.user.role import UserRoles
from authorization.domain.value_object.user.id import UserId


class PyJWTTokenProvider(ITokenProvider):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minute: int,
        refresh_token_expire_day: int,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_ttl = timedelta(minutes=access_token_expire_minute)
        self._refresh_ttl = timedelta(days=refresh_token_expire_day)

    def create_access_token(self, user_id: UserId, role: UserRoles) -> str:
        return self._issue_token(user_id, role, self._access_ttl, "access")

    def create_refresh_token(self, user_id: UserId, role: UserRoles) -> str:
        return self._issue_token(user_id, role, self._refresh_ttl, "refresh")

    def get_user_id_from_token(
        self, token: str, token_type: TokenType = "access"
    ) -> UserId:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            actual_type = payload.get("type")
            if actual_type != token_type:
                raise InvalidTokenError(
                    f"Token type mismatch. Expected '{token_type}', got '{actual_type}'"
                )

            return UserId(int(payload["sub"]))
        except (jwt.PyJWTError, KeyError, ValueError) as e:
            raise InvalidTokenError("Invalid or expired token.") from e

    def get_user_role_from_token(
        self, token: str, token_type: TokenType = "access"
    ) -> UserRoles:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            actual_type = payload.get("type")
            if actual_type != token_type:
                raise InvalidTokenError(
                    f"Token type mismatch. Expected '{token_type}', got '{actual_type}'"
                )

            return UserRoles(payload["role"])
        except (jwt.PyJWTError, KeyError, ValueError) as e:
            raise InvalidTokenError("Invalid or expired token.") from e

    def _issue_token(
        self,
        user_id: UserId,
        role: UserRoles,
        expire_delta: timedelta,
        token_type: TokenType,
    ) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id.value),
            "role": str(role),
            "exp": now + expire_delta,
            "iat": now,
            "type": token_type,
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
