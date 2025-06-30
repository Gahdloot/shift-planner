from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class ScheduleBase(BaseModel):
    name: str
    year: int
    month: int
    notes: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    organization_id: int


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None  # draft, finalized, archived


class Schedule(ScheduleBase):
    id: int
    organization_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScheduleAssignmentBase(BaseModel):
    employee_id: int
    date: date
    shift_position: int
    notes: Optional[str] = None


class ScheduleAssignmentCreate(ScheduleAssignmentBase):
    schedule_id: int


class ScheduleAssignmentUpdate(BaseModel):
    employee_id: Optional[int] = None
    shift_position: Optional[int] = None
    notes: Optional[str] = None
    is_manual_override: Optional[bool] = None


class ScheduleAssignment(ScheduleAssignmentBase):
    id: int
    schedule_id: int
    is_manual_override: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScheduleWithAssignments(Schedule):
    assignments: List[ScheduleAssignment] = []


class ScheduleGenerationRequest(BaseModel):
    organization_id: int
    year: int
    month: int
    shift_pattern_id: int
    name: Optional[str] = None 