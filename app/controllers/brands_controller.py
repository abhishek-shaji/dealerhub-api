from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.models.brand_model import BrandCreate, BrandResponse
from app.schemas import User, Brand
from app.database import get_db
from app.services.brands_service import BrandService, get_brand_service
from app.utilities.auth_utility import get_current_user

router = APIRouter(prefix="/brands")


@cbv(router)
class BrandsController:
    db: Session = Depends(get_db)
    brand_service: BrandService = Depends(get_brand_service)

    @router.post(
        "/",
        status_code=201,
        response_model=BrandResponse,
        description="Create a new brand",
    )
    def create_brand(
        self,
        form_data: BrandCreate,
        current_user: User = Depends(get_current_user),
    ):
        return self.brand_service.create(form_data, current_user)

    @router.get(
        "/",
        status_code=200,
        response_model=List[BrandResponse],
        description="Get a list of brands for the current user",
    )
    def get_brands(
        self,
        current_user: User = Depends(get_current_user),
    ):
        return self.brand_service.get_all(current_user)

    @router.get(
        "/{brand_id}",
        status_code=200,
        response_model=BrandResponse,
        description="Get a brand by its ID",
    )
    def get_brand(
        self,
        brand_id: UUID,
        current_user: User = Depends(get_current_user),
    ):
        return self.brand_service.get_one(brand_id, current_user)

    @router.put(
        "/{brand_id}",
        status_code=200,
        response_model=BrandResponse,
        description="Update an existing brand",
    )
    def update_brand(
        self,
        brand_id: UUID,
        form_data: BrandCreate,
        current_user: User = Depends(get_current_user),
    ):
        return self.brand_service.update(brand_id, form_data, current_user)

    @router.delete(
        "/{brand_id}",
        status_code=204,
        description="Delete a brand",
    )
    def delete_brand(
        self,
        brand_id: UUID,
        current_user: User = Depends(get_current_user),
    ):
        self.brand_service.delete(brand_id, current_user)
        return
