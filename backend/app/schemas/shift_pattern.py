from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ShiftPatternBase(BaseModel):
    name: str
    description: Optional[str] = None
    pattern_data: Dict[str, Any]
    shifts_per_day: int = 3


class ShiftPatternCreate(ShiftPatternBase):
    organization_id: int


class ShiftPatternUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    pattern_data: Optional[Dict[str, Any]] = None
    shifts_per_day: Optional[int] = None
    is_active: Optional[bool] = None


class ShiftPattern(ShiftPatternBase):
    id: int
    organization_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Pattern data examples
class PatternExample(BaseModel):
    """Example pattern data structure"""
    work_days: int  # e.g., 4 for 4 days on
    rest_days: int  # e.g., 2 for 2 days off
    cycle_length: int  # e.g., 6 for 4+2 pattern 