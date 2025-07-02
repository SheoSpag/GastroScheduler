from fastapi import APIRouter, Depends, Response, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.shift import ShiftCreate, ShiftOut, ShiftUpdate
from app.crud.shift import get_shift as shift_get, get_all_shifts as all_shifts_get, create_shift as shift_create, delete_shift as shift_delete, update_shift as shift_update

router = APIRouter()

@router.get("/{shift_id}", response_model=ShiftOut, status_code=status.HTTP_200_OK)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    return shift_get(db, shift_id)
    

@router.get("/", response_model=List[ShiftOut], status_code=status.HTTP_200_OK)
def get_all_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_shifts = all_shifts_get(db, skip=skip, limit=limit)
    if not all_shifts:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return all_shifts

@router.post("/", response_model=ShiftOut, status_code=status.HTTP_201_CREATED)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    return shift_create(db, shift)

@router.patch("/{shift_id}", response_model=ShiftOut)
def update_shift(shift_id: int, shift: ShiftUpdate, db: Session = Depends(get_db)):
    return shift_update(db, shift_id, shift)

@router.delete("/{shift_id}", response_model=ShiftOut, status_code=status.HTTP_200_OK)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    return shift_delete(db, shift_id)
    