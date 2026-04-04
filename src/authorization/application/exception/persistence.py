from authorization.application.exception.common import ApplicationError


class PersistenceError(ApplicationError):
    pass


class PersistenceConnectionError(PersistenceError):
    pass


class ReaderError(PersistenceError):
    pass


class WriterError(PersistenceError):
    pass
