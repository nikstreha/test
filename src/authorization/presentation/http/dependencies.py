from dishka.integrations.fastapi import FromDishka, inject
from fastapi import HTTPException, Request, status

from authorization.application.exception.auth import InvalidTokenError
from authorization.application.port.security.token_provider import ITokenProvider
from authorization.presentation.http.middleware.rate_limit import LoginRateLimiter


@inject
async def check_login_rate_limit(
    request: Request,
    rate_limiter: FromDishka[LoginRateLimiter],
) -> None:
    await rate_limiter(request)


@inject
async def get_current_user_id(
    request: Request,
    token_provider: FromDishka[ITokenProvider],
) -> int:
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found",
        )
    access_token = auth_header[7:]
    try:
        user_id_vo = token_provider.get_user_id_from_token(
            access_token, token_type="access"
        )
        return user_id_vo.value  # type: ignore
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        ) from e
