from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class EmployeeShiftPattern(Base):
    __tablename__ = "employee_shift_patterns"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_pattern_id = Column(Integer, ForeignKey("shift_patterns.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 