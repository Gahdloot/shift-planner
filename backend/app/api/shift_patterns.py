from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..crud import shift_pattern as shift_pattern_crud
from ..schemas.shift_pattern import ShiftPattern, ShiftPatternCreate, ShiftPatternUpdate
from .auth import get_current_user
from ..schemas.user import User

router = APIRouter()


@router.post("/", response_model=ShiftPattern)
def create_shift_pattern(
    shift_pattern: ShiftPatternCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return shift_pattern_crud.create_shift_pattern(db=db, shift_pattern=shift_pattern)


@router.get("/organization/{organization_id}", response_model=List[ShiftPattern])
def read_shift_patterns_by_organization(
    organization_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shift_patterns = shift_pattern_crud.get_shift_patterns_by_organization(
        db, organization_id=organization_id, skip=skip, limit=limit
    )
    return shift_patterns


@router.get("/{shift_pattern_id}", response_model=ShiftPattern)
def read_shift_pattern(
    shift_pattern_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shift_pattern = shift_pattern_crud.get_shift_pattern(db, shift_pattern_id=shift_pattern_id)
    if shift_pattern is None:
        raise HTTPException(status_code=404, detail="Shift pattern not found")
    return shift_pattern


@router.put("/{shift_pattern_id}", response_model=ShiftPattern)
def update_shift_pattern(
    shift_pattern_id: int,
    shift_pattern: ShiftPatternUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_shift_pattern = shift_pattern_crud.update_shift_pattern(
        db, shift_pattern_id=shift_pattern_id, shift_pattern=shift_pattern
    )
    if db_shift_pattern is None:
        raise HTTPException(status_code=404, detail="Shift pattern not found")
    return db_shift_pattern


@router.delete("/{shift_pattern_id}")
def delete_shift_pattern(
    shift_pattern_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shift_pattern = shift_pattern_crud.delete_shift_pattern(db, shift_pattern_id=shift_pattern_id)
    if shift_pattern is None:
        raise HTTPException(status_code=404, detail="Shift pattern not found")
    return {"message": "Shift pattern deleted successfully"} 