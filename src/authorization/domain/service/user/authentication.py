from authorization.domain.entity.user import User
from authorization.domain.port.security.password_hasher import IPasswordHasher
from authorization.domain.value_object.user.raw_password import RawPassword


class UserAuthenticationService:
    def __init__(self, *, password_hasher: IPasswordHasher) -> None:
        self._password_hasher = password_hasher

    async def authenticate(self, *, user: User, raw_password: RawPassword) -> bool:
        if not user.is_active:
            return False

        password_match = await self._password_hasher.verify(
            raw_password=raw_password, hashed_password=user.password_hash
        )

        return password_match
