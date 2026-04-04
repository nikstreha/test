from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UpdateUserRequest(BaseModel):
    full_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=20)


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str | None
    phone: str | None
    role: str
    is_active: bool
    created_at: datetime
