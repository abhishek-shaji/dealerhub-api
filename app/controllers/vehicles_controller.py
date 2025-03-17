from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.models.vehicle_model import VehicleCreate, VehicleResponse
from app.schemas import User
from app.utilities.auth_utility import get_current_user
from app.services.vehicles_service import VehiclesService, get_vehicles_service

router = APIRouter(prefix="/vehicles")


@cbv(router)
class VehiclesController:
    vehicles_service: VehiclesService = Depends(get_vehicles_service)

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
        return self.vehicles_service.create(form_data, current_user)

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
        return self.vehicles_service.get_all(current_user)

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
        return self.vehicles_service.get_one(vehicle_id, current_user)

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
        return self.vehicles_service.update(vehicle_id, form_data, current_user)

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
        return self.vehicles_service.delete(vehicle_id, current_user) 