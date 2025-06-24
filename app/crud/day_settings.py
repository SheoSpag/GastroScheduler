from sqlalchemy.orm import Session
from app.schemas.day_settings import SettingsCreate, SettingsUpdate

def get_one_day_settings(db: Session, branch_id: int, week_day: int):
    from app.models.day_settings import DaySettings
    
    return db.query(DaySettings).filter(DaySettings.branch_id == branch_id, DaySettings.week_day == week_day).first()

def get_all_branch_days_settings(db:Session, branch_id: int):
    from app.models.day_settings import DaySettings
    
    return db.query(DaySettings).filter(DaySettings.branch_id == branch_id).all()

def update_day_settings(db: Session, branch_id: int, week_day: int, day_settings: SettingsUpdate):
    searched_day = get_one_day_settings(db, branch_id, week_day)
    if not searched_day:
        return None
    
    update_data = day_settings.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(searched_day, key, value)
        
    db.commit()
    db.refresh(searched_day)
    return searched_day



