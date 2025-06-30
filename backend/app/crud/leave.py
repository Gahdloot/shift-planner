from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import date
from ..models.leave import Leave
from ..schemas.leave import LeaveCreate, LeaveUpdate


def get_leave(db: Session, leave_id: int):
    return db.query(Leave).filter(Leave.id == leave_id).first()


def get_leaves_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(Leave).filter(
        Leave.employee_id == employee_id,
        Leave.is_active == True
    ).offset(skip).limit(limit).all()


def get_active_leaves_by_date_range(db: Session, employee_id: int, start_date: date, end_date: date):
    """Get all active leaves that overlap with the given date range"""
    return db.query(Leave).filter(
        and_(
            Leave.employee_id == employee_id,
            Leave.is_active == True,
            Leave.start_date <= end_date,
            Leave.end_date >= start_date
        )
    ).all()


def create_leave(db: Session, leave: LeaveCreate):
    db_leave = Leave(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


def update_leave(db: Session, leave_id: int, leave: LeaveUpdate):
    db_leave = get_leave(db, leave_id)
    if not db_leave:
        return None
    
    update_data = leave.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_leave, field, value)
    
    db.commit()
    db.refresh(db_leave)
    return db_leave


def delete_leave(db: Session, leave_id: int):
    db_leave = get_leave(db, leave_id)
    if db_leave:
        db_leave.is_active = False
        db.commit()
    return db_leave


def is_employee_on_leave(db: Session, employee_id: int, check_date: date):
    """Check if an employee is on leave on a specific date"""
    leave = db.query(Leave).filter(
        and_(
            Leave.employee_id == employee_id,
            Leave.is_active == True,
            Leave.start_date <= check_date,
            Leave.end_date >= check_date
        )
    ).first()
    return leave is not None 