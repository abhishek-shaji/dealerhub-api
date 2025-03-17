from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.vehicle_model import VehicleCreate, VehicleResponse
from app.schemas import User, Vehicle, Brand
from app.database import get_db
from app.services.base_service import BaseService


class VehiclesService(BaseService):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, current_user: User):
        vehicles = (
            self.db.query(Vehicle)
            .filter(Vehicle.created_by_id == current_user.id)
            .all()
        )
        return vehicles

    def get_one(self, id: UUID, current_user: User):
        vehicle = (
            self.db.query(Vehicle)
            .filter(
                Vehicle.id == id,
                Vehicle.created_by_id == current_user.id,
            )
            .first()
        )

        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        return vehicle

    def create(self, form_data: VehicleCreate, current_user: User):
        brand = self.db.query(Brand).filter(Brand.id == form_data.brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        vehicle = Vehicle(
            registration_number=form_data.registration_number,
            vin_number=form_data.vin_number,
            is_new=form_data.is_new,
            kms_driven=form_data.kms_driven,
            brand_id=form_data.brand_id,
            model=form_data.model,
            price=form_data.price,
            first_registration=form_data.first_registration,
            created_by_id=current_user.id,
        )
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)

        return vehicle

    def update(self, id: UUID, form_data: VehicleCreate, current_user: User):
        brand = self.db.query(Brand).filter(Brand.id == form_data.brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        vehicle = self.get_one(id, current_user)

        vehicle.registration_number = form_data.registration_number
        vehicle.vin_number = form_data.vin_number
        vehicle.is_new = form_data.is_new
        vehicle.kms_driven = form_data.kms_driven
        vehicle.brand_id = form_data.brand_id
        vehicle.model = form_data.model
        vehicle.price = form_data.price
        vehicle.first_registration = form_data.first_registration
        vehicle.updated_by_id = current_user.id

        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, id: UUID, current_user: User):
        vehicle = self.get_one(id, current_user)

        self.db.delete(vehicle)
        self.db.commit()

        return


def get_vehicles_service(db: Session = Depends(get_db)):
    return VehiclesService(db) 