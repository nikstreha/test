from authorization.application.exception.common import ApplicationError


class AuthError(ApplicationError):
    pass


class UserAlreadyExistError(AuthError):
    pass


class InvalidCredentialError(AuthError):
    pass


class InvalidTokenError(AuthError):
    pass
