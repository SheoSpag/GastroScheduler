from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.area import AreaCreate, AreaOut, AreaUpdate
from app.crud.area import get_area as area_get, get_areas as areas_get, create_area as area_create, update_area as area_update, delete_area as area_delete

router = APIRouter()

@router.get("/", response_model=List[AreaOut], status_code=status.HTTP_200_OK)
def get_areas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_areas = areas_get(db, skip=skip, limit=limit)
    
    if not all_areas:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    return all_areas

@router.get("/{area_id}", response_model=AreaOut, status_code=status.HTTP_200_OK)
def get_area(area_id: int, db: Session = Depends(get_db)):
    return area_get(db, area_id)

@router.post("/", response_model=AreaOut, status_code=status.HTTP_201_CREATED)
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    return area_create(db, area)

@router.patch("/{area_id}", response_model=AreaOut, status_code=status.HTTP_200_OK)
def update_area(area_id: int, area: AreaUpdate, db: Session = Depends(get_db)):
    return area_update(db, area_id, area)
    
@router.delete("/{area_id}", response_model=AreaOut)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    return area_delete(db, area_id)
    
    