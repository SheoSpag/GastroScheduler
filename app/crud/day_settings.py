from sqlalchemy.orm import Session
from app.schemas.day_settings import SettingsUpdate
from app.crud.branch import get_branch
from fastapi import status
from app.exceptions.customError import CustomError
from app.utils.error_handler import handle_exception


def get_day_settings(db: Session, branch_id: int, week_day: int):
    from app.models.day_settings import DaySettings
    try:
        #Only 4 validation
        get_branch(db, branch_id)
        searched_day_setting = db.query(DaySettings).filter(DaySettings.branch_id == branch_id, DaySettings.week_day == week_day).first()
    
        if not searched_day_setting:
            raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Day settings not found")
    
        return searched_day_setting
    except Exception as e:
        handle_exception(e, "Internal error while getting the day settings")

def get_all_branch_days_settings(db:Session, branch_id: int):
    from app.models.day_settings import DaySettings
    try:
            
        #Only 4 validation
        get_branch(db, branch_id)
        
        return db.query(DaySettings).filter(DaySettings.branch_id == branch_id).all()
    except Exception as e:
        handle_exception(e, "Internal error while getting barnch all day settings")

def update_day_settings(db: Session, branch_id: int, week_day: int, day_settings: SettingsUpdate):
    try:
        searched_day_settings = get_day_settings(db, branch_id, week_day)
        
        update_data = day_settings.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(searched_day_settings, key, value)
            
        db.commit()
        db.refresh(searched_day_settings)
        return searched_day_settings
    
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the day settings")




