from authorization.domain.exception.base import DomainError


class UserError(DomainError):
    pass


class UserEmailInvalidError(UserError):
    pass


class UserNameInvalidError(UserError):
    pass


class PhoneInvalidError(UserError):
    pass


class UserIsActiveInvalidError(UserError):
    pass


class PasswordError(UserError):
    pass


class PasswordInvalidError(PasswordError):
    pass


class PasswordHashInvalidError(PasswordError):
    pass


class CurrentPasswordInvalidError(PasswordError):
    def __init__(self) -> None:
        super().__init__("Current password does not match")


class UserIsNotActiveError(UserError):
    pass
