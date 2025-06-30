from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class ShiftPattern(Base):
    __tablename__ = "shift_patterns"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    pattern_data = Column(Text, nullable=False)  # JSON string defining the pattern
    shifts_per_day = Column(Integer, default=3)  # Number of shifts per day
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="shift_patterns")
    employees = relationship("Employee", secondary="employee_shift_patterns") 