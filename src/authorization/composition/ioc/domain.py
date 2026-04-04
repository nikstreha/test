from dishka import Provider, Scope, provide

from authorization.domain.port.security.password_hasher import IPasswordHasher
from authorization.domain.service.user.authentication import UserAuthenticationService
from authorization.domain.service.user.registration import UserRegistrationService


class DomainProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_registration_service(
        self,
        password_hasher: IPasswordHasher,
    ) -> UserRegistrationService:
        return UserRegistrationService(password_hasher=password_hasher)

    @provide
    def get_user_authentication_service(
        self,
        password_hasher: IPasswordHasher,
    ) -> UserAuthenticationService:
        return UserAuthenticationService(password_hasher=password_hasher)
