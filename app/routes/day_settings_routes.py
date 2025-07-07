from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session 

from app.db.db import get_db
from app.schemas.day_settings import SettingsUpdate, SettingsOut
from app.crud.day_settings import get_day_settings as onde_day_settings_get, get_all_branch_days_settings as all_branch_settings_get, update_day_settings as day_settings_update
from app.crud.branch import get_branch as branch_get

router = APIRouter()

@router.get("/{week_day}/branch/{branch_id}", response_model=SettingsOut, status_code=status.HTTP_200_OK)
def get_one_day_settings(branch_id: int, week_day: int, db: Session = Depends(get_db)):
    return onde_day_settings_get(db, branch_id, week_day)

@router.get("/branch/{branch_id}", response_model=List[SettingsOut])
def get_branch_all_days_settings(branch_id: int, db: Session = Depends(get_db)):
    return all_branch_settings_get(db, branch_id)

@router.patch("/{week_day}/branch/{branch_id}", response_model=SettingsOut)
def update_day_settings(branch_id: int, week_day: int, base_intensity: SettingsUpdate, db: Session = Depends(get_db)):
    return day_settings_update(db, branch_id, week_day, base_intensity)
     
     
