from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.models.organization_model import OrganizationCreate, OrganizationResponse
from app.schemas import User
from app.database import get_db
from app.utilities.auth_utility import get_current_user
from app.services.organizations_service import OrganizationService, get_organization_service

router = APIRouter(prefix="/organizations")


@cbv(router)
class OrganizationsController:
    db: Session = Depends(get_db)
    organization_service: OrganizationService = Depends(get_organization_service)

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
        return self.organization_service.create(form_data, current_user)

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
        return self.organization_service.get_all(current_user)

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
        return self.organization_service.get_one(organization_id, current_user)

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
        return self.organization_service.update(organization_id, form_data, current_user)

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
        self.organization_service.delete(organization_id, current_user)
        return
