from sqlalchemy.orm import Session
from app.schemas.base_intensity import IntensityCreate, IntensityUpdate

def get_intensity(db: Session, branch_id: int, week_day: int):
    from app.models.base_intensity import BaseIntensity
    
    return db.query(BaseIntensity).filter(BaseIntensity.branch_id == branch_id, BaseIntensity.week_day == week_day).first()

def get_branch_intensities(db:Session, branch_id: int):
    from app.models.base_intensity import BaseIntensity
    
    return db.query(BaseIntensity).filter(BaseIntensity.branch_id == branch_id).all()

def update_intensity(db: Session, branch_id: int, week_day: int, base_intensity: IntensityUpdate):
    searched_intensity = get_intensity(db, branch_id, week_day)
    if not searched_intensity:
        return None
    
    update_data = base_intensity.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(searched_intensity, key, value)
        
    db.commit()
    db.refresh(searched_intensity)
    return searched_intensity



