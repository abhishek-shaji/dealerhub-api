from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr = Field(
        description="User's email address",
        examples=["john.doe@example.com"]
    )
    firstname: str = Field(
        description="User's first name",
        min_length=1,
        max_length=50,
        examples=["John"]
    )
    lastname: str = Field(
        description="User's last name",
        min_length=1,
        max_length=50,
        examples=["Doe"]
    )
    password: str = Field(
        description="User's password",
        min_length=8,
        examples=["strongPassword123"]
    )

    class Config:
        schema_extra = {
            "description": "Schema for creating a new user"
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(
        description="User's email address for login",
        examples=["john.doe@example.com"]
    )
    password: str = Field(
        description="User's password for login",
        min_length=8,
        examples=["strongPassword123"]
    )

    class Config:
        schema_extra = {
            "description": "Schema for user login credentials"
        }


class UserResponse(BaseModel):
    id: int = Field(
        description="Unique identifier for the user",
        examples=[1]
    )
    email: EmailStr = Field(
        description="User's email address",
        examples=["john.doe@example.com"]
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "description": "Schema for user response data",
            "example": {
                "id": 1,
                "email": "john.doe@example.com"
            }
        }