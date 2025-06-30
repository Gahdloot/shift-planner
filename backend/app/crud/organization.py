from sqlalchemy.orm import Session
from ..models.organization import Organization
from ..schemas.organization import OrganizationCreate, OrganizationUpdate


def get_organization(db: Session, organization_id: int):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organization).offset(skip).limit(limit).all()


def create_organization(db: Session, organization: OrganizationCreate):
    db_organization = Organization(**organization.dict())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization


def update_organization(db: Session, organization_id: int, organization: OrganizationUpdate):
    db_organization = get_organization(db, organization_id)
    if not db_organization:
        return None
    
    update_data = organization.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_organization, field, value)
    
    db.commit()
    db.refresh(db_organization)
    return db_organization


def delete_organization(db: Session, organization_id: int):
    db_organization = get_organization(db, organization_id)
    if db_organization:
        db.delete(db_organization)
        db.commit()
    return db_organization 