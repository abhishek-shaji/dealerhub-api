from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.models.brand_model import BrandCreate, BrandResponse
from app.schemas import User, Brand
from app.database import get_db
from app.utilities.auth_utility import get_current_user

router = APIRouter(prefix="/brands")


@cbv(router)
class BrandsController:
    db: Session = Depends(get_db)

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
        brand = Brand(
            name=form_data.name,
            created_by_id=current_user.id,
        )
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand

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
        brands = (
            self.db.query(Brand)
            .filter(Brand.created_by_id == current_user.id)
            .all()
        )
        return brands

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
        brand = (
            self.db.query(Brand)
            .filter(
                Brand.id == brand_id,
                Brand.created_by_id == current_user.id,
            )
            .first()
        )
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        return brand

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
        brand = (
            self.db.query(Brand)
            .filter(
                Brand.id == brand_id,
                Brand.created_by_id == current_user.id,
            )
            .first()
        )
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        brand.name = form_data.name
        self.db.commit()
        self.db.refresh(brand)
        return brand

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
        brand = (
            self.db.query(Brand)
            .filter(
                Brand.id == brand_id,
                Brand.created_by_id == current_user.id,
            )
            .first()
        )

        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        self.db.delete(brand)
        self.db.commit()

        return 