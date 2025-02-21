from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, UUID4


class OrganizationCreate(BaseModel):
    name: str = Field(
        description="Organization's name",
        min_length=1,
        max_length=50,
        examples=["FastCars Inc."],
    )
    email: EmailStr = Field(
        description="Organization's email address", examples=["john.doe@example.com"]
    )

    class Config:
        schema_extra = {"description": "Schema for creating a new organization"}


class OrganizationResponse(BaseModel):
    id: UUID4 = Field(
        description="Unique identifier for the organization", examples=[1]
    )
    name: str = Field(
        description="Organization's name",
        min_length=1,
        max_length=50,
        examples=["John"],
    )
    email: EmailStr = Field(
        description="Organization's email address", examples=["john.doe@example.com"]
    )
    created_at: datetime = Field(
        description="Date and time the organization was created",
        examples=["2025-02-21T11:04:48.476531"],
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "description": "Schema for organization response data",
            "example": {"id": 1, "email": "john.doe@example.com"},
        }
