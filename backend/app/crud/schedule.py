from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from ..models.schedule import Schedule
from ..models.schedule_assignment import ScheduleAssignment
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleAssignmentCreate, ScheduleAssignmentUpdate


def get_schedule(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def get_schedules_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(Schedule).filter(
        Schedule.organization_id == organization_id
    ).offset(skip).limit(limit).all()


def get_schedule_with_assignments(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def create_schedule(db: Session, schedule: ScheduleCreate):
    db_schedule = Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def update_schedule(db: Session, schedule_id: int, schedule: ScheduleUpdate):
    db_schedule = get_schedule(db, schedule_id)
    if not db_schedule:
        return None
    
    update_data = schedule.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_schedule, field, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_schedule(db: Session, schedule_id: int):
    db_schedule = get_schedule(db, schedule_id)
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
    return db_schedule


def create_schedule_assignment(db: Session, assignment: ScheduleAssignmentCreate):
    db_assignment = ScheduleAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def update_schedule_assignment(db: Session, assignment_id: int, assignment: ScheduleAssignmentUpdate):
    db_assignment = db.query(ScheduleAssignment).filter(ScheduleAssignment.id == assignment_id).first()
    if not db_assignment:
        return None
    
    update_data = assignment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def delete_schedule_assignment(db: Session, assignment_id: int):
    db_assignment = db.query(ScheduleAssignment).filter(ScheduleAssignment.id == assignment_id).first()
    if db_assignment:
        db.delete(db_assignment)
        db.commit()
    return db_assignment


def get_assignments_by_schedule(db: Session, schedule_id: int):
    return db.query(ScheduleAssignment).filter(ScheduleAssignment.schedule_id == schedule_id).all()


def get_assignments_by_date_range(db: Session, schedule_id: int, start_date, end_date):
    return db.query(ScheduleAssignment).filter(
        and_(
            ScheduleAssignment.schedule_id == schedule_id,
            ScheduleAssignment.date >= start_date,
            ScheduleAssignment.date <= end_date
        )
    ).all() 