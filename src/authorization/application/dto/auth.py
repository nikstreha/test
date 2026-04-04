from dataclasses import dataclass

from authorization.application.dto.user import UserResponseDTO


@dataclass(frozen=True)
class UserSignUpRequestDTO:
    email: str
    password: str
    full_name: str | None
    phone: str | None
    ip: str


@dataclass(frozen=True)
class TokensResponseDTO:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class UserSignUpResponseDTO:
    tokens: TokensResponseDTO
    user: UserResponseDTO


@dataclass(frozen=True)
class UserSignInRequestDTO:
    email: str
    password: str
    ip: str


@dataclass(frozen=True)
class UserSignInResponseDTO:
    tokens: TokensResponseDTO
    user: UserResponseDTO


@dataclass(frozen=True)
class UserRefreshTokenRequestDTO:
    refresh_token: str


@dataclass(frozen=True)
class UserRefreshTokenResponseDTO:
    access_token: str
    refresh_token: str
