from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class LeaveBase(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str] = None
    notes: Optional[str] = None


class LeaveCreate(LeaveBase):
    employee_id: int


class LeaveUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class Leave(LeaveBase):
    id: int
    employee_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 