from fastapi import APIRouter

from authorization.presentation.http.auth.router import router as auth_router
from authorization.presentation.http.user.router import router as user_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
