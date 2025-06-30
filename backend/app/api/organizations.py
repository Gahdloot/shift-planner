from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..crud import organization as organization_crud
from ..schemas.organization import Organization, OrganizationCreate, OrganizationUpdate
from .auth import get_current_user
from ..schemas.user import User

router = APIRouter()


@router.post("/", response_model=Organization)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return organization_crud.create_organization(db=db, organization=organization)


@router.get("/", response_model=List[Organization])
def read_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organizations = organization_crud.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/{organization_id}", response_model=Organization)
def read_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization = organization_crud.get_organization(db, organization_id=organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.put("/{organization_id}", response_model=Organization)
def update_organization(
    organization_id: int,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_organization = organization_crud.update_organization(
        db, organization_id=organization_id, organization=organization
    )
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


@router.delete("/{organization_id}")
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization = organization_crud.delete_organization(db, organization_id=organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"message": "Organization deleted successfully"} 