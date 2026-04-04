from collections.abc import AsyncGenerator, Iterator
from typing import cast

from dishka import Provider, Scope, provide

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
from authorization.composition.configuration.settings import Settings
from authorization.domain.port.security.password_hasher import IPasswordHasher
from authorization.infrastructure.persistence.sqla.repository.audit_log.writer import (
    SQLAAuditLogWriter,
)
from authorization.infrastructure.persistence.sqla.repository.user.reader import (
    SQLAUserReader,
)
from authorization.infrastructure.persistence.sqla.repository.user.writer import (
    SQLAUserWriter,
)
from authorization.infrastructure.persistence.sqla.session_proxy import SessionProxy
from authorization.infrastructure.persistence.sqla.sqla_persistence_connector import (
    SQLAPersistenceConnector,
)
from authorization.infrastructure.persistence.sqla.sqla_uow import SQLAUnitOfWork
from authorization.infrastructure.persistence.sqla.type import (
    ReaderSession,
    WriterSession,
)
from authorization.infrastructure.security.password_hasher.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from authorization.infrastructure.security.password_hasher.type import (
    PasswordHasherSemaphore,
    PasswordHasherThreadPoolExecutor,
)
from authorization.infrastructure.security.token_provider.jwt_token_provider import (
    PyJWTTokenProvider,
)


class PersistenceSessionProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_persistence_connector(
        self,
        s: Settings,
    ) -> AsyncGenerator[SQLAPersistenceConnector]:
        connector = SQLAPersistenceConnector(
            dsn=s.postgres_dsn,
            echo=s.POSTGRES_ECHO,
            echo_pool=s.POSTGRES_ECHO_POOL,
            pool_size=s.POSTGRES_POOL_SIZE,
            max_overflow=s.POSTGRES_MAX_OVERFLOW,
        )
        await connector.connect()
        yield connector
        await connector.disconnect()

    @provide(scope=Scope.REQUEST)
    def get_uow(self, connector: SQLAPersistenceConnector) -> IUnitOfWork:
        return SQLAUnitOfWork(session_factory=connector.session_factory)

    @provide(scope=Scope.REQUEST)
    async def get_reader_session(
        self, connector: SQLAPersistenceConnector
    ) -> AsyncGenerator[ReaderSession]:
        async with connector.session_factory() as session:
            yield cast(ReaderSession, session)

    @provide(scope=Scope.REQUEST)
    def get_writer_session(self, uow: IUnitOfWork) -> WriterSession:
        sqla_uow = cast(SQLAUnitOfWork, uow)
        session_proxy = SessionProxy(uow=sqla_uow)
        return cast(WriterSession, cast(object, session_proxy))


class PersistenceRepositoryProvider(Provider):
    scope = Scope.REQUEST

    # --- User ---
    @provide
    def get_audit_log_writer(self, session: WriterSession) -> IAuditLogWriter:
        return SQLAAuditLogWriter(session=session)

    @provide
    def get_user_writer(self, session: WriterSession) -> IUserWriter:
        return SQLAUserWriter(session=session)

    @provide
    def get_user_reader(self, session: ReaderSession) -> IUserReader:
        return SQLAUserReader(session=session)


def persistence_provider() -> tuple[Provider, ...]:
    return (
        PersistenceRepositoryProvider(),
        PersistenceSessionProvider(),
    )


class PasswordHasherProvider(Provider):
    scope = Scope.APP

    @provide
    def get_hasher_semaphore(self, s: Settings) -> PasswordHasherSemaphore:
        return PasswordHasherSemaphore(s.PASSWORD_HASHER_CONCURRENCY_LIMIT)

    @provide
    def get_hasher_executor(
        self, s: Settings
    ) -> Iterator[PasswordHasherThreadPoolExecutor]:
        executor = PasswordHasherThreadPoolExecutor(
            max_workers=s.PASSWORD_HASHER_THREAD_POOL_SIZE,
            thread_name_prefix="bcrypt_password_hasher",
        )
        yield executor
        executor.shutdown(wait=True)

    @provide
    def get_password_hasher(
        self,
        s: Settings,
        executor: PasswordHasherThreadPoolExecutor,
        semaphore: PasswordHasherSemaphore,
    ) -> IPasswordHasher:
        return BcryptPasswordHasher(
            pepper=s.PASSWORD_HASHER_PEPPER,
            executor=executor,
            semaphore=semaphore,
            wait_timeout_s=s.PASSWORD_HASHER_WAIT_TIMEOUT_S,
        )


class TokenProvider(Provider):
    scope = Scope.APP

    @provide
    def get_token_provider(self, s: Settings) -> ITokenProvider:
        return PyJWTTokenProvider(
            secret_key=s.TOKEN_SECRET_KEY,
            algorithm=s.TOKEN_ALGORITHM,
            access_token_expire_minute=s.TOKEN_ACCESS_EXPIRE_MINUTE,
            refresh_token_expire_day=s.TOKEN_REFRESH_EXPIRE_DAY,
        )


def security_provider() -> tuple[Provider, ...]:
    return (PasswordHasherProvider(), TokenProvider())


def _infrastructure_provider() -> tuple[Provider, ...]:
    return (
        *persistence_provider(),
        *security_provider(),
    )
