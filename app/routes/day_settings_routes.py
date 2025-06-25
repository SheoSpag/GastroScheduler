from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session 

from app.db.db import get_db
from app.schemas.day_settings import SettingsCreate, SettingsUpdate, SettingsOut
from app.crud.day_settings import get_one_day_settings as onde_day_settings_get, get_all_branch_days_settings as all_branch_settings_get, update_day_settings as day_settings_update
from app.crud.branch import get_branch as branch_get

router = APIRouter()

@router.get("/{branch_id}/{week_day}", response_model=SettingsOut, status_code=status.HTTP_200_OK)
def get_one_day_settings(branch_id: int, week_day: int, db: Session = Depends(get_db)):
    searched_branch = branch_get(db, branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    searched_settings = onde_day_settings_get(db, branch_id, week_day)
    if not searched_settings:
        raise HTTPException(status_code=404, detail="Day settings not found")
    return searched_settings

@router.get("/{branch_id}", response_model=List[SettingsOut])
def get_all_branch_days_settings(branch_id: int, db: Session = Depends(get_db)):
    searched_branch = branch_get(db, branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    branch_settings = all_branch_settings_get(db, branch_id)
    return branch_settings

@router.patch("/{branch_id}/{week_day}", response_model=SettingsOut)
def update_day_settings(branch_id: int, week_day: int, base_intensity: SettingsUpdate, db: Session = Depends(get_db)):
    searched_branch = branch_get(db, branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    searched_settings = onde_day_settings_get(db, branch_id, week_day)
    if not searched_settings:
        raise HTTPException(status_code=404, detail="Day setting not found")
    
    updated_intensity = day_settings_update(db, branch_id, week_day, base_intensity)
    return updated_intensity
    