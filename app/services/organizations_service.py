from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.organization_model import OrganizationCreate, OrganizationResponse
from app.schemas import Organization, User
from app.services.base_service import BaseService


class OrganizationService(BaseService):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, current_user: User):
        organizations = (
            self.db.query(Organization)
            .filter(Organization.created_by_id == current_user.id)
            .all()
        )

        return organizations

    def get_one(self, id: UUID, current_user: User):
        organization = (
            self.db.query(Organization)
            .filter(
                Organization.id == id,
                Organization.created_by_id == current_user.id,
            )
            .first()
        )
        
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
            
        return organization

    def create(self, form_data: OrganizationCreate, current_user: User):
        organization = Organization(
            name=form_data.name,
            email=str(form_data.email),
            created_by_id=current_user.id,
        )

        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def update(self, id: UUID, form_data: OrganizationCreate, current_user: User):
        organization = self.get_one(id, current_user)

        organization.name = form_data.name
        organization.email = str(form_data.email)
        
        self.db.commit()
        self.db.refresh(organization)
        
        return organization

    def delete(self, id: UUID, current_user: User):
        organization = self.get_one(id, current_user)
            
        self.db.delete(organization)
        self.db.commit()
        
        return None


def get_organization_service(db: Session = Depends(get_db)):
    return OrganizationService(db) 