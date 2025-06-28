from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.area import AreaCreate, AreaOut, AreaUpdate
from app.crud.area import get_area as area_get, get_areas as areas_get, create_area as area_create, update_area as area_update, delete_area as area_delete

router = APIRouter()

@router.get("/", response_model=List[AreaOut], status_code=status.HTTP_200_OK)
def get_areas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_areas = areas_get(db, skip=skip, limit=limit)
    return all_areas

@router.get("/{area_id}", response_model=AreaOut, status_code=status.HTTP_200_OK)
def get_area(area_id: int, db: Session = Depends(get_db)):
    searched_area = area_get(db, area_id)
    if not searched_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return searched_area

@router.post("/", response_model=AreaOut, status_code=status.HTTP_201_CREATED)
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    created_area = area_create(db, area)
    return created_area

@router.patch("/{area_id}", response_model=AreaOut, status_code=status.HTTP_200_OK)
def update_area(area_id: int, area: AreaUpdate, db: Session = Depends(get_db)):
    updated_area = area_update(db, area_id, area)
    if not updated_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return updated_area

@router.delete("/{area_id}", response_model=AreaOut)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    deleted_area = area_delete(db, area_id)
    if not deleted_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return deleted_area
    
    