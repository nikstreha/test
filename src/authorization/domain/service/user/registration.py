from authorization.domain.entity.user import User
from authorization.domain.enum.user.role import UserRoles
from authorization.domain.port.security.password_hasher import IPasswordHasher
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.full_name import FullUserName
from authorization.domain.value_object.user.phone import UserPhone
from authorization.domain.value_object.user.raw_password import RawPassword


class UserRegistrationService:
    def __init__(
        self,
        *,
        password_hasher: IPasswordHasher,
    ) -> None:
        self._password_hasher = password_hasher

    async def register(
        self,
        *,
        email: UserEmail,
        password: RawPassword,
        role: UserRoles = UserRoles.FREE_USER,
        full_name: FullUserName | None = None,
        phone: UserPhone | None = None,
    ) -> User:
        password_hash = await self._password_hasher.hash(raw_password=password)

        return User.create(
            email=email,
            password_hash=password_hash,
            role=role,
            full_name=full_name,
            phone=phone,
        )
