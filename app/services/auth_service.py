import os
from datetime import datetime, timedelta

from jose import jwt
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.schemas import User
from app.database import get_db
from app.models.user_model import UserCreate, UserResponse, UserLogin
from app.config import config
from app.services.base_service import BaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def register(self, user: UserCreate):
        existing_user = self.db.query(User).filter(User.email == user.email).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            email=str(user.email),
            password=hashed_password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def login(self, user: UserLogin, response: Response):
        db_user = self.db.query(User).filter(User.email == user.email).first()

        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        access_token_expires = datetime.utcnow() + timedelta(minutes=1440)
        access_token = jwt.encode(
            {"sub": str(db_user.email), "exp": access_token_expires},
            config.SECRET_KEY,
            algorithm="HS256",
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=1800,
        )

        return db_user

    def logout(self, response: Response):
        response.delete_cookie(
            key="access_token", httponly=True, secure=True, samesite="lax"
        )
        return {"message": "Successfully logged out"}


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db) 