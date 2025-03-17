from fastapi import APIRouter, Depends, Response
from fastapi_utils.cbv import cbv

from app.models.user_model import UserCreate, UserResponse, UserLogin
from app.services.auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/auth")


@cbv(router)
class AuthController:
    auth_service: AuthService = Depends(get_auth_service)

    @router.post(
        "/register",
        response_model=UserResponse,
        description="Register a new user",
    )
    def register(self, user: UserCreate):
        return self.auth_service.register(user)

    @router.post("/login", response_model=UserResponse)
    def login(self, user: UserLogin, response: Response):
        return self.auth_service.login(user, response)

    @router.post("/logout")
    def logout(self, response: Response):
        return self.auth_service.logout(response)
