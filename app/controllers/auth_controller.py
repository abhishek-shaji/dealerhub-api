import os
from datetime import datetime, timedelta

from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User
from app.database import SessionLocal, get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@cbv(router)
class AuthController:
    db: Session = Depends(get_db)

    @router.post("/register", response_model=UserResponse)
    def register(self, user: UserCreate):
        existing_user = self.db.query(User).filter(User.email == user.email).first()

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

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

    @router.post("/login", response_model=UserResponse)
    def login(self, user: UserLogin, response: Response):
        db_user = self.db.query(User).filter(User.email == user.email).first()

        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token_expires = datetime.utcnow() + timedelta(minutes=1440)
        access_token = jwt.encode(
            {
                "sub": str(db_user.email),
                "exp": access_token_expires
            },
            os.getenv('SECRET_KEY'),
            algorithm="HS256"
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

    @router.post("/logout")
    def logout(self, response: Response):
        response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return {"message": "Successfully logged out"}