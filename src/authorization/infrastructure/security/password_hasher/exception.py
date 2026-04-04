from authorization.application.exception.common import (
    ApplicationError,
    TransientError,
)


class PasswordHasherIsBusyError(TransientError):
    pass


class PasswordHasherError(ApplicationError):
    pass
