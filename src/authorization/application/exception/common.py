class ApplicationError(Exception):
    pass


class TransientError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    pass
