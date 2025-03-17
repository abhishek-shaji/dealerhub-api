from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.brand_model import BrandCreate, BrandResponse
from app.schemas import Brand, User
from app.services.base_service import BaseService


class BrandService(BaseService):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, current_user: User):
        brands = (
            self.db.query(Brand).filter(Brand.created_by_id == current_user.id).all()
        )

        return brands

    def get_one(self, id: UUID, current_user: User):
        brand = self.db.query(Brand).filter(Brand.id == id, Brand.created_by_id == current_user.id).first()

        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        
        return brand

    def create(self, form_data: BrandCreate, current_user: User):
        brand = Brand(
            name=form_data.name,
            created_by_id=current_user.id,
        )

        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)

        return brand

    def update(self, id: UUID, data: BrandCreate, current_user: User):
        brand = self.get_one(id, current_user)
        
        brand.name = data.name
        self.db.commit()
        self.db.refresh(brand)

        return brand

    def delete(self, id: UUID, current_user: User):
        brand = self.get_one(id, current_user)
        
        self.db.delete(brand)
        self.db.commit()

        return


def get_brand_service(db: Session = Depends(get_db)):
    return BrandService(db)
