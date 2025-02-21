import os
from datetime import datetime, timedelta

from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.schemas import User
from app.database import get_db
from app.models.user_model import UserCreate, UserResponse, UserLogin
from app.config import config

router = APIRouter(prefix="/cars")


@cbv(router)
class AuthController:
    db: Session = Depends(get_db)

    @router.get("/")
    def getCars(self, response: Response):
        return {"message": "Successfully logged out"}
