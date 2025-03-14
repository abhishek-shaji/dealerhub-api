from datetime import datetime

from pydantic import BaseModel, Field, UUID4


class BrandCreate(BaseModel):
    name: str = Field(
        description="Brand's name",
        min_length=1,
        max_length=50,
        examples=["Toyota"],
    )

    class Config:
        schema_extra = {"description": "Schema for creating a new brand"}


class BrandResponse(BaseModel):
    id: UUID4 = Field(
        description="Unique identifier for the brand", examples=[1]
    )
    name: str = Field(
        description="Brand's name",
        min_length=1,
        max_length=50,
        examples=["Toyota"],
    )
    created_at: datetime = Field(
        description="Date and time the brand was created",
        examples=["2025-02-21T11:04:48.476531"],
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "description": "Schema for brand response data",
            "example": {"id": 1, "name": "Toyota"},
        } 