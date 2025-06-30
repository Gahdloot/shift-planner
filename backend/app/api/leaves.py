from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..core.database import get_db
from ..crud import leave as leave_crud
from ..schemas.leave import Leave, LeaveCreate, LeaveUpdate
from .auth import get_current_user
from ..schemas.user import User

router = APIRouter()


@router.post("/", response_model=Leave)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return leave_crud.create_leave(db=db, leave=leave)


@router.get("/employee/{employee_id}", response_model=List[Leave])
def read_leaves_by_employee(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leaves = leave_crud.get_leaves_by_employee(
        db, employee_id=employee_id, skip=skip, limit=limit
    )
    return leaves


@router.get("/{leave_id}", response_model=Leave)
def read_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leave = leave_crud.get_leave(db, leave_id=leave_id)
    if leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave


@router.put("/{leave_id}", response_model=Leave)
def update_leave(
    leave_id: int,
    leave: LeaveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_leave = leave_crud.update_leave(
        db, leave_id=leave_id, leave=leave
    )
    if db_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    return db_leave


@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leave = leave_crud.delete_leave(db, leave_id=leave_id)
    if leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    return {"message": "Leave deleted successfully"} 
 