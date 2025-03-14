from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, UUID4


class VehicleCreate(BaseModel):
    registration_number: str = Field(
        description="Vehicle's registration number",
        min_length=1,
        max_length=50,
        examples=["ABC123"],
    )
    vin_number: str = Field(
        description="Vehicle's VIN number",
        min_length=1,
        max_length=50,
        examples=["1HGCM82633A123456"],
    )
    is_new: bool = Field(
        description="Whether the vehicle is new or used",
        examples=[False],
    )
    kms_driven: int = Field(
        description="Kilometers driven by the vehicle",
        ge=0,
        examples=[50000],
    )
    brand_id: UUID4 = Field(
        description="ID of the brand of the vehicle",
    )
    model: str = Field(
        description="Model of the vehicle",
        min_length=1,
        max_length=50,
        examples=["Corolla"],
    )
    price: float = Field(
        description="Price of the vehicle",
        gt=0,
        examples=[25000.50],
    )
    first_registration: date = Field(
        description="Date of first registration",
        examples=["2020-01-01"],
    )

    class Config:
        schema_extra = {"description": "Schema for creating a new vehicle"}


class VehicleResponse(BaseModel):
    id: UUID4 = Field(
        description="Unique identifier for the vehicle", examples=[1]
    )
    registration_number: str = Field(
        description="Vehicle's registration number",
        examples=["ABC123"],
    )
    vin_number: str = Field(
        description="Vehicle's VIN number",
        examples=["1HGCM82633A123456"],
    )
    is_new: bool = Field(
        description="Whether the vehicle is new or used",
        examples=[False],
    )
    kms_driven: int = Field(
        description="Kilometers driven by the vehicle",
        examples=[50000],
    )
    brand_id: UUID4 = Field(
        description="ID of the brand of the vehicle",
    )
    model: str = Field(
        description="Model of the vehicle",
        examples=["Corolla"],
    )
    price: float = Field(
        description="Price of the vehicle",
        examples=[25000.50],
    )
    first_registration: date = Field(
        description="Date of first registration",
        examples=["2020-01-01"],
    )
    created_at: datetime = Field(
        description="Date and time the vehicle was created",
        examples=["2025-02-21T11:04:48.476531"],
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "description": "Schema for vehicle response data",
            "example": {
                "id": 1,
                "registration_number": "ABC123",
                "vin_number": "1HGCM82633A123456",
                "is_new": False,
                "kms_driven": 50000,
                "brand_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "model": "Corolla",
                "price": 25000.50,
                "first_registration": "2020-01-01",
            },
        } 