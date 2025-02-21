from fastapi import Request, Depends, HTTPException
from jose import jwt, JWTError
from app.config import config
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import User

ALGORITHM = "HS256"


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_email: int = payload.get("sub")

        if user_email is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = db.query(User).filter(User.email == user_email).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
