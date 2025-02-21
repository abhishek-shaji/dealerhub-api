from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.models.organization_model import OrganizationCreate, OrganizationResponse
from app.schemas import User, Organization
from app.database import get_db
from app.utilities.auth_utility import get_current_user

router = APIRouter(prefix="/organizations")


@cbv(router)
class OrganizationsController:
    db: Session = Depends(get_db)

    @router.post(
        "/",
        status_code=201,
        response_model=OrganizationResponse,
        description="Create a new organization",
    )
    def create_organization(
        self,
        form_data: OrganizationCreate,
        current_user: User = Depends(get_current_user),
    ):
        organization = Organization(
            name=form_data.name,
            email=str(form_data.email),
            created_by_id=current_user.id,
        )
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    @router.get(
        "/",
        status_code=200,
        response_model=List[OrganizationResponse],
        description="Get a list of organizations for the current user",
    )
    def get_organizations(
        self,
        current_user: User = Depends(get_current_user),
    ):
        organizations = (
            self.db.query(Organization)
            .filter(Organization.created_by_id == current_user.id)
            .all()
        )
        return organizations

    @router.get(
        "/{organization_id}",
        status_code=200,
        response_model=OrganizationResponse,
        description="Get an organization by its ID",
    )
    def get_organization(
        self,
        organization_id: UUID,
        current_user: User = Depends(get_current_user),
    ):
        organization = (
            self.db.query(Organization)
            .filter(
                Organization.id == organization_id,
                Organization.created_by_id == current_user.id,
            )
            .first()
        )
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        return organization

    @router.put(
        "/{organization_id}",
        status_code=200,
        response_model=OrganizationResponse,
        description="Update an existing organization",
    )
    def update_organization(
        self,
        organization_id: UUID,
        form_data: OrganizationCreate,
        current_user: User = Depends(get_current_user),
    ):
        organization = (
            self.db.query(Organization)
            .filter(
                Organization.id == organization_id,
                Organization.created_by_id == current_user.id,
            )
            .first()
        )
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        organization.name = form_data.name
        organization.email = str(form_data.email)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    @router.delete(
        "/{organization_id}",
        status_code=204,
        description="Delete an organization",
    )
    def delete_organization(
        self,
        organization_id: UUID,
        current_user: User = Depends(get_current_user),
    ):
        organization = (
            self.db.query(Organization)
            .filter(
                Organization.id == organization_id,
                Organization.created_by_id == current_user.id,
            )
            .first()
        )

        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        self.db.delete(organization)
        self.db.commit()

        return
