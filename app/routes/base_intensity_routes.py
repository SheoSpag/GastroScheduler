from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import Session 

from app.db.db import get_db
from app.schemas.base_intensity import IntensityCreate, IntensityUpdate, IntensityOut
from app.crud.base_intensity import get_intensity as intensity_get, get_branch_intensities as branch_intensities_get, update_intensity as intensity_update
from app.crud.branch import get_branch as branch_get

router = APIRouter()

@router.get("/{branch_id}/{week_day}", response_model=IntensityOut, status_code=status.HTTP_200_OK)
def get_intensity(branch_id: int, week_day: int, db: Session = Depends(get_db)):
    searched_branch = branch_get(db, branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    searched_intensity = intensity_get(db, branch_id, week_day)
    if not searched_intensity:
        raise HTTPException(status_code=404, detail="Base Intensity not found")
    return searched_intensity

@router.get("/{branch_id}", response_model=List[IntensityOut])
def get_branch_intensities(branch_id: int, db: Session = Depends(get_db)):
    searched_branch = branch_get(db, branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    branch_intensities = branch_intensities_get(db, branch_id)
    return branch_intensities

@router.patch("/{branch_id}/{week_day}", response_model=IntensityOut)
def update_branch_intensity(branch_id: int, week_day: int, base_intensity: IntensityUpdate, db: Session = Depends(get_db)):
    searched_branch = branch_get(db, branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    searched_intensity = intensity_get(db, branch_id, week_day)
    if not searched_intensity:
        raise HTTPException(status_code=404, detail="Base Intensity not found")
    
    updated_intensity = intensity_update(db, branch_id, week_day, base_intensity)
    return updated_intensity
    