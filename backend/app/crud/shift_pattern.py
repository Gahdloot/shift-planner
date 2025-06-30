from sqlalchemy.orm import Session
import json
from ..models.shift_pattern import ShiftPattern
from ..schemas.shift_pattern import ShiftPatternCreate, ShiftPatternUpdate


def get_shift_pattern(db: Session, shift_pattern_id: int):
    return db.query(ShiftPattern).filter(ShiftPattern.id == shift_pattern_id).first()


def get_shift_patterns_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(ShiftPattern).filter(
        ShiftPattern.organization_id == organization_id,
        ShiftPattern.is_active == True
    ).offset(skip).limit(limit).all()


def create_shift_pattern(db: Session, shift_pattern: ShiftPatternCreate):
    # Convert pattern_data dict to JSON string
    shift_pattern_data = shift_pattern.dict()
    shift_pattern_data["pattern_data"] = json.dumps(shift_pattern_data["pattern_data"])
    
    db_shift_pattern = ShiftPattern(**shift_pattern_data)
    db.add(db_shift_pattern)
    db.commit()
    db.refresh(db_shift_pattern)
    return db_shift_pattern


def update_shift_pattern(db: Session, shift_pattern_id: int, shift_pattern: ShiftPatternUpdate):
    db_shift_pattern = get_shift_pattern(db, shift_pattern_id)
    if not db_shift_pattern:
        return None
    
    update_data = shift_pattern.dict(exclude_unset=True)
    if "pattern_data" in update_data:
        update_data["pattern_data"] = json.dumps(update_data["pattern_data"])
    
    for field, value in update_data.items():
        setattr(db_shift_pattern, field, value)
    
    db.commit()
    db.refresh(db_shift_pattern)
    return db_shift_pattern


def delete_shift_pattern(db: Session, shift_pattern_id: int):
    db_shift_pattern = get_shift_pattern(db, shift_pattern_id)
    if db_shift_pattern:
        db_shift_pattern.is_active = False
        db.commit()
    return db_shift_pattern


def get_shift_pattern_data(db: Session, shift_pattern_id: int):
    """Get shift pattern data as a dictionary"""
    shift_pattern = get_shift_pattern(db, shift_pattern_id)
    if shift_pattern and shift_pattern.pattern_data:
        try:
            return json.loads(shift_pattern.pattern_data)
        except json.JSONDecodeError:
            return {}
    return {} 