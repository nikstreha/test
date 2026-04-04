from dishka import Provider, Scope, provide

from authorization.application.command.auth.refresh_token import (
    RefreshTokenInteractor,
)
from authorization.application.command.auth.sign_in import SignInInteractor
from authorization.application.command.auth.sign_up import SignUpInteractor
from authorization.application.command.user.update_user_data import (
    UpdateUserDataInteractor,
)
from authorization.application.port.persistence.repository.audit_log.writer import (
    IAuditLogWriter,
)
from authorization.application.port.persistence.repository.user.reader import (
    IUserReader,
)
from authorization.application.port.persistence.repository.user.writer import (
    IUserWriter,
)
from authorization.application.port.persistence.uow import IUnitOfWork
from authorization.application.port.security.token_provider import ITokenProvider
from authorization.application.query.user.get_user_data import GetUserDataInteractor
from authorization.domain.service.user.authentication import (
    UserAuthenticationService,
)
from authorization.domain.service.user.registration import UserRegistrationService


class QueryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_profile_query(self, user_reader: IUserReader) -> GetUserDataInteractor:
        return GetUserDataInteractor(user_reader=user_reader)


class CommandProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_sign_up_interactor(
        self,
        uow: IUnitOfWork,
        user_writer: IUserWriter,
        audit_log_writer: IAuditLogWriter,
        user_registration_service: UserRegistrationService,
        token_provider: ITokenProvider,
    ) -> SignUpInteractor:
        return SignUpInteractor(
            uow=uow,
            user_writer=user_writer,
            audit_log_writer=audit_log_writer,
            user_registration_service=user_registration_service,
            token_provider=token_provider,
        )

    @provide
    def get_sign_in_interactor(
        self,
        uow: IUnitOfWork,
        user_writer: IUserWriter,
        audit_log_writer: IAuditLogWriter,
        user_authentication_service: UserAuthenticationService,
        token_provider: ITokenProvider,
    ) -> SignInInteractor:
        return SignInInteractor(
            uow=uow,
            user_writer=user_writer,
            audit_log_writer=audit_log_writer,
            user_authentication_service=user_authentication_service,
            token_provider=token_provider,
        )

    @provide
    def get_refresh_token_interactor(
        self,
        token_provider: ITokenProvider,
        user_reader: IUserReader,
    ) -> RefreshTokenInteractor:
        return RefreshTokenInteractor(
            token_provider=token_provider,
            user_reader=user_reader,
        )

    @provide
    def get_update_user_data_interactor(
        self,
        uow: IUnitOfWork,
        user_writer: IUserWriter,
        user_reader: IUserReader,
    ) -> UpdateUserDataInteractor:
        return UpdateUserDataInteractor(
            uow=uow, user_writer=user_writer, user_reader=user_reader
        )


def _application_provider() -> tuple[Provider, ...]:
    return (
        QueryProvider(),
        CommandProvider(),
    )
