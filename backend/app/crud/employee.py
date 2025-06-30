from sqlalchemy.orm import Session
from sqlalchemy import and_
import json
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(Employee).filter(
        Employee.organization_id == organization_id,
        Employee.is_active == True
    ).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate):
    # Convert preferences dict to JSON string if provided
    employee_data = employee.dict()
    if employee_data.get("preferences"):
        employee_data["preferences"] = json.dumps(employee_data["preferences"])
    
    db_employee = Employee(**employee_data)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    
    update_data = employee.dict(exclude_unset=True)
    if "preferences" in update_data and update_data["preferences"]:
        update_data["preferences"] = json.dumps(update_data["preferences"])
    
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db_employee.is_active = False
        db.commit()
    return db_employee


def get_employee_preferences(db: Session, employee_id: int):
    """Get employee preferences as a dictionary"""
    employee = get_employee(db, employee_id)
    if employee and employee.preferences:
        try:
            return json.loads(employee.preferences)
        except json.JSONDecodeError:
            return {}
    return {} 