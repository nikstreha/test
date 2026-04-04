from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Request

from authorization.application.command.auth.refresh_token import RefreshTokenInteractor
from authorization.application.command.auth.sign_in import SignInInteractor
from authorization.application.command.auth.sign_up import SignUpInteractor
from authorization.application.dto.auth import (
    UserRefreshTokenRequestDTO,
    UserSignInRequestDTO,
    UserSignUpRequestDTO,
)
from authorization.presentation.http.auth.schema import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokensSchema,
)
from authorization.presentation.http.dependencies import check_login_rate_limit
from authorization.presentation.http.util.get_ip import get_client_ip

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=AuthResponse)
@inject
async def register(
    request: Request,
    body: RegisterRequest,
    interactor: FromDishka[SignUpInteractor],
) -> AuthResponse:
    result = await interactor(
        UserSignUpRequestDTO(
            email=str(body.email),
            password=body.password,
            full_name=body.full_name,
            phone=body.phone,
            ip=get_client_ip(request),
        )
    )
    return AuthResponse.model_validate(result)


@router.post(
    "/login",
    response_model=AuthResponse,
    dependencies=[Depends(check_login_rate_limit)],
)
@inject
async def login(
    request: Request,
    body: LoginRequest,
    interactor: FromDishka[SignInInteractor],
) -> AuthResponse:
    result = await interactor(
        UserSignInRequestDTO(
            email=str(body.email),
            password=body.password,
            ip=get_client_ip(request),
        )
    )
    return AuthResponse.model_validate(result)


@router.post("/refresh", response_model=TokensSchema)
@inject
async def refresh(
    body: RefreshRequest,
    interactor: FromDishka[RefreshTokenInteractor],
) -> TokensSchema:
    result = await interactor(
        UserRefreshTokenRequestDTO(refresh_token=body.refresh_token)
    )
    return TokensSchema.model_validate(result)
