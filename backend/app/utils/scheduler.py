import random
import json
from datetime import date, datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.schedule import Schedule
from ..models.schedule_assignment import ScheduleAssignment
from ..models.employee import Employee
from ..models.shift_pattern import ShiftPattern
from ..crud import schedule as schedule_crud, leave as leave_crud


def generate_schedule(
    db: Session,
    organization_id: int,
    year: int,
    month: int,
    shift_pattern: ShiftPattern,
    employees: List[Employee],
    name: str
) -> Schedule:
    """Generate a complete schedule for a month based on shift pattern and employees"""
    
    # Create the schedule
    schedule_data = {
        "organization_id": organization_id,
        "name": name,
        "year": year,
        "month": month,
        "status": "draft"
    }
    
    schedule = schedule_crud.create_schedule(db, schedule_data)
    
    # Parse shift pattern data
    pattern_data = json.loads(shift_pattern.pattern_data)
    shifts_per_day = shift_pattern.shifts_per_day
    
    # Get all dates in the month
    month_dates = get_month_dates(year, month)
    
    # Generate assignments for each date
    for current_date in month_dates:
        # Skip weekends if specified in pattern
        if pattern_data.get("skip_weekends", False) and current_date.weekday() >= 5:
            continue
        
        # Determine which employees should work on this date based on pattern
        working_employees = get_working_employees_for_date(
            employees, current_date, pattern_data, db
        )
        
        # Assign shifts for this date
        for shift_position in range(1, shifts_per_day + 1):
            if working_employees:
                # Randomly select an employee for this shift
                employee = random.choice(working_employees)
                working_employees.remove(employee)  # Remove to avoid double assignment
                
                # Create assignment
                assignment_data = {
                    "schedule_id": schedule.id,
                    "employee_id": employee.id,
                    "date": current_date,
                    "shift_position": shift_position,
                    "is_manual_override": False
                }
                
                schedule_crud.create_schedule_assignment(db, assignment_data)
    
    return schedule


def get_month_dates(year: int, month: int) -> List[date]:
    """Get all dates in a given month"""
    dates = []
    _, last_day = calendar.monthrange(year, month)
    
    for day in range(1, last_day + 1):
        dates.append(date(year, month, day))
    
    return dates


def get_working_employees_for_date(
    employees: List[Employee],
    current_date: date,
    pattern_data: Dict[str, Any],
    db: Session
) -> List[Employee]:
    """Determine which employees should work on a given date based on pattern"""
    
    working_employees = []
    
    for employee in employees:
        # Skip if employee is on leave
        if leave_crud.is_employee_on_leave(db, employee.id, current_date):
            continue
        
        # Check if employee should work based on pattern
        if should_employee_work_on_date(employee, current_date, pattern_data):
            working_employees.append(employee)
    
    return working_employees


def should_employee_work_on_date(
    employee: Employee,
    current_date: date,
    pattern_data: Dict[str, Any]
) -> bool:
    """Determine if an employee should work on a specific date based on pattern"""
    
    # Get pattern parameters
    work_days = pattern_data.get("work_days", 4)
    rest_days = pattern_data.get("rest_days", 2)
    cycle_length = work_days + rest_days
    
    # Calculate days since a reference date (e.g., start of year)
    reference_date = date(current_date.year, 1, 1)
    days_since_reference = (current_date - reference_date).days
    
    # Calculate position in cycle
    position_in_cycle = days_since_reference % cycle_length
    
    # Employee should work if within work days portion of cycle
    return position_in_cycle < work_days


def apply_employee_preferences(
    assignments: List[ScheduleAssignment],
    employees: List[Employee]
) -> List[ScheduleAssignment]:
    """Apply employee preferences to shift assignments"""
    
    # Create a mapping of employee preferences
    employee_prefs = {}
    for employee in employees:
        if employee.preferences:
            try:
                prefs = json.loads(employee.preferences)
                employee_prefs[employee.id] = prefs
            except json.JSONDecodeError:
                continue
    
    # Apply preferences by swapping assignments where beneficial
    for i, assignment in enumerate(assignments):
        employee_pref = employee_prefs.get(assignment.employee_id, {})
        preferred_shifts = employee_pref.get("preferred_shifts", [])
        
        # If employee has a preference for this shift position, try to keep it
        if assignment.shift_position in preferred_shifts:
            continue
        
        # Look for opportunities to swap with other assignments
        for j, other_assignment in enumerate(assignments):
            if i == j:
                continue
            
            # Check if swap would be beneficial for both employees
            if would_swap_be_beneficial(assignment, other_assignment, employee_prefs):
                # Perform swap
                temp_shift = assignment.shift_position
                assignment.shift_position = other_assignment.shift_position
                other_assignment.shift_position = temp_shift
    
    return assignments


def would_swap_be_beneficial(
    assignment1: ScheduleAssignment,
    assignment2: ScheduleAssignment,
    employee_prefs: Dict[int, Dict]
) -> bool:
    """Check if swapping two assignments would be beneficial for both employees"""
    
    pref1 = employee_prefs.get(assignment1.employee_id, {})
    pref2 = employee_prefs.get(assignment2.employee_id, {})
    
    preferred_shifts1 = pref1.get("preferred_shifts", [])
    preferred_shifts2 = pref2.get("preferred_shifts", [])
    
    # Check if swap would improve both employees' preferences
    current_score1 = 1 if assignment1.shift_position in preferred_shifts1 else 0
    current_score2 = 1 if assignment2.shift_position in preferred_shifts2 else 0
    
    potential_score1 = 1 if assignment2.shift_position in preferred_shifts1 else 0
    potential_score2 = 1 if assignment1.shift_position in preferred_shifts2 else 0
    
    # Swap is beneficial if total preference score increases
    current_total = current_score1 + current_score2
    potential_total = potential_score1 + potential_score2
    
    return potential_total > current_total


# Import calendar at the top level
import calendar 