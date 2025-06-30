from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class EmployeeBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class EmployeeCreate(EmployeeBase):
    organization_id: int


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase):
    id: int
    organization_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 