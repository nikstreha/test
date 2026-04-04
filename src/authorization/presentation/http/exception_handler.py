import structlog
from fastapi import FastAPI, Request, status

logger = structlog.get_logger(__name__)
from fastapi.responses import JSONResponse

from authorization.application.exception.auth import (
    InvalidCredentialError,
    InvalidTokenError,
    UserAlreadyExistError,
)
from authorization.application.exception.common import ApplicationError, TransientError
from authorization.application.exception.user import UserNotFound


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistError)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidCredentialError)
    async def invalid_credential_handler(request: Request, exc: InvalidCredentialError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request: Request, exc: UserNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TransientError)
    async def transient_error_handler(request: Request, exc: TransientError):
        logger.error("error.transient", error=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError):
        logger.warning("error.application", error=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )
