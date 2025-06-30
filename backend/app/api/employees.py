from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..crud import employee as employee_crud
from ..schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from .auth import get_current_user
from ..schemas.user import User

router = APIRouter()


@router.post("/", response_model=Employee)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return employee_crud.create_employee(db=db, employee=employee)


@router.get("/organization/{organization_id}", response_model=List[Employee])
def read_employees_by_organization(
    organization_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employees = employee_crud.get_employees_by_organization(
        db, organization_id=organization_id, skip=skip, limit=limit
    )
    return employees


@router.get("/{employee_id}", response_model=Employee)
def read_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = employee_crud.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_employee = employee_crud.update_employee(
        db, employee_id=employee_id, employee=employee
    )
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = employee_crud.delete_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"} 