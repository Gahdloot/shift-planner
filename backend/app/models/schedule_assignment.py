from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class ScheduleAssignment(Base):
    __tablename__ = "schedule_assignments"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    shift_position = Column(Integer, nullable=False)  # 1, 2, 3 for first, second, third shift
    is_manual_override = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedule = relationship("Schedule", back_populates="assignments")
    employee = relationship("Employee", back_populates="schedule_assignments") 