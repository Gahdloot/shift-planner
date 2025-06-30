from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
import calendar
import random
from ..core.database import get_db
from ..crud import schedule as schedule_crud, employee as employee_crud, shift_pattern as shift_pattern_crud, leave as leave_crud
from ..schemas.schedule import (
    Schedule, ScheduleCreate, ScheduleUpdate, 
    ScheduleAssignment, ScheduleAssignmentCreate, ScheduleAssignmentUpdate,
    ScheduleWithAssignments, ScheduleGenerationRequest
)
from .auth import get_current_user
from ..schemas.user import User
from ..utils.scheduler import generate_schedule
from ..utils.export import export_schedule_to_excel, export_schedule_to_pdf

router = APIRouter()


@router.post("/generate", response_model=Schedule)
def generate_new_schedule(
    request: ScheduleGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a new schedule based on shift pattern and employees"""
    # Get shift pattern
    shift_pattern = shift_pattern_crud.get_shift_pattern(db, request.shift_pattern_id)
    if not shift_pattern:
        raise HTTPException(status_code=404, detail="Shift pattern not found")
    
    # Get employees for the organization
    employees = employee_crud.get_employees_by_organization(db, request.organization_id)
    if not employees:
        raise HTTPException(status_code=400, detail="No employees found for organization")
    
    # Generate schedule
    schedule = generate_schedule(
        db=db,
        organization_id=request.organization_id,
        year=request.year,
        month=request.month,
        shift_pattern=shift_pattern,
        employees=employees,
        name=request.name or f"Schedule {request.year}-{request.month:02d}"
    )
    
    return schedule


@router.get("/organization/{organization_id}", response_model=List[Schedule])
def read_schedules_by_organization(
    organization_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    schedules = schedule_crud.get_schedules_by_organization(
        db, organization_id=organization_id, skip=skip, limit=limit
    )
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleWithAssignments)
def read_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    schedule = schedule_crud.get_schedule_with_assignments(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.put("/{schedule_id}", response_model=Schedule)
def update_schedule(
    schedule_id: int,
    schedule: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_schedule = schedule_crud.update_schedule(
        db, schedule_id=schedule_id, schedule=schedule
    )
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule


@router.post("/{schedule_id}/finalize", response_model=Schedule)
def finalize_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Finalize a draft schedule"""
    schedule = schedule_crud.get_schedule(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    if schedule.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft schedules can be finalized")
    
    schedule.status = "finalized"
    db.commit()
    db.refresh(schedule)
    return schedule


@router.put("/{schedule_id}/assignments/{assignment_id}", response_model=ScheduleAssignment)
def update_schedule_assignment(
    schedule_id: int,
    assignment_id: int,
    assignment: ScheduleAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually override a schedule assignment"""
    db_assignment = schedule_crud.update_schedule_assignment(
        db, assignment_id=assignment_id, assignment=assignment
    )
    if db_assignment is None:
        raise HTTPException(status_code=404, detail="Schedule assignment not found")
    
    # Mark as manual override
    db_assignment.is_manual_override = True
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.get("/{schedule_id}/export/excel")
def export_schedule_excel(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export schedule to Excel"""
    schedule = schedule_crud.get_schedule_with_assignments(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return export_schedule_to_excel(schedule)


@router.get("/{schedule_id}/export/pdf")
def export_schedule_pdf(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export schedule to PDF"""
    schedule = schedule_crud.get_schedule_with_assignments(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return export_schedule_to_pdf(schedule)


@router.get("/{schedule_id}/statistics")
def get_schedule_statistics(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get shift distribution statistics for a schedule"""
    schedule = schedule_crud.get_schedule_with_assignments(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Calculate statistics
    stats = {}
    for assignment in schedule.assignments:
        employee_name = assignment.employee.name
        if employee_name not in stats:
            stats[employee_name] = {"total_shifts": 0, "shifts_by_position": {}}
        
        stats[employee_name]["total_shifts"] += 1
        shift_pos = assignment.shift_position
        if shift_pos not in stats[employee_name]["shifts_by_position"]:
            stats[employee_name]["shifts_by_position"][shift_pos] = 0
        stats[employee_name]["shifts_by_position"][shift_pos] += 1
    
    return {
        "schedule_id": schedule_id,
        "total_assignments": len(schedule.assignments),
        "employee_statistics": stats
    } 