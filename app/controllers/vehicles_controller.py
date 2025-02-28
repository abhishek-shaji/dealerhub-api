from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.models.vehicle_model import VehicleCreate, VehicleResponse
from app.schemas import User, Vehicle, Brand
from app.database import get_db
from app.utilities.auth_utility import get_current_user

router = APIRouter(prefix="/vehicles")


@cbv(router)
class VehiclesController:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        status_code=201,
        response_model=VehicleResponse,
        description="Create a new vehicle",
    )
    def create_vehicle(
        self,
        form_data: VehicleCreate,
        current_user: User = Depends(get_current_user),
    ):
        # Check if brand exists
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

    @router.get(
        "/",
        status_code=200,
        response_model=List[VehicleResponse],
        description="Get a list of vehicles for the current user",
    )
    def get_vehicles(
        self,
        current_user: User = Depends(get_current_user),
    ):
        vehicles = (
            self.db.query(Vehicle)
            .filter(Vehicle.created_by_id == current_user.id)
            .all()
        )
        return vehicles

    @router.get(
        "/{vehicle_id}",
        status_code=200,
        response_model=VehicleResponse,
        description="Get a vehicle by its ID",
    )
    def get_vehicle(
        self,
        vehicle_id: UUID,
        current_user: User = Depends(get_current_user),
    ):
        vehicle = (
            self.db.query(Vehicle)
            .filter(
                Vehicle.id == vehicle_id,
                Vehicle.created_by_id == current_user.id,
            )
            .first()
        )
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    @router.put(
        "/{vehicle_id}",
        status_code=200,
        response_model=VehicleResponse,
        description="Update an existing vehicle",
    )
    def update_vehicle(
        self,
        vehicle_id: UUID,
        form_data: VehicleCreate,
        current_user: User = Depends(get_current_user),
    ):
        # Check if brand exists
        brand = self.db.query(Brand).filter(Brand.id == form_data.brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        vehicle = (
            self.db.query(Vehicle)
            .filter(
                Vehicle.id == vehicle_id,
                Vehicle.created_by_id == current_user.id,
            )
            .first()
        )
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")

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

    @router.delete(
        "/{vehicle_id}",
        status_code=204,
        description="Delete a vehicle",
    )
    def delete_vehicle(
        self,
        vehicle_id: UUID,
        current_user: User = Depends(get_current_user),
    ):
        vehicle = (
            self.db.query(Vehicle)
            .filter(
                Vehicle.id == vehicle_id,
                Vehicle.created_by_id == current_user.id,
            )
            .first()
        )

        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        self.db.delete(vehicle)
        self.db.commit()

        return 