from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from authorization.application.command.user.update_user_data import (
    UpdateUserDataInteractor,
)
from authorization.application.dto.user import UpdateUserDataRequestDTO
from authorization.application.query.user.get_user_data import GetUserDataInteractor
from authorization.presentation.http.dependencies import get_current_user_id
from authorization.presentation.http.user.schema import (
    UpdateUserRequest,
    UserProfileResponse,
)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserProfileResponse)
@inject
async def get_me(
    query: FromDishka[GetUserDataInteractor],
    user_id: int = Depends(get_current_user_id),
) -> UserProfileResponse:
    result = await query(user_id=user_id)
    return UserProfileResponse.model_validate(result)


@router.put("/me", response_model=UserProfileResponse)
@inject
async def update_me(
    body: UpdateUserRequest,
    interactor: FromDishka[UpdateUserDataInteractor],
    user_id: int = Depends(get_current_user_id),
) -> UserProfileResponse:
    result = await interactor(
        UpdateUserDataRequestDTO(
            user_id=user_id,
            full_name=body.full_name,
            phone=body.phone,
        )
    )
    return UserProfileResponse.model_validate(result)
