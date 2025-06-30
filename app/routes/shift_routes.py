from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.shift import ShiftCreate, ShiftOut, ShiftUpdate
from app.crud.shift import get_shift as shift_get, get_all_shifts as all_shifts_get, create_shift as shift_create, delete_shift as shift_delete, update_shift as shift_update

router = APIRouter()

@router.get("/{shift_id}", response_model=ShiftOut, status=status.HTTP_200_OK)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    searched_shift = shift_get(db, shift_id)
    if not searched_shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    return searched_shift

@router.get("/", response_model=List[ShiftOut], status_code=status.HTTP_200_OK)
def get_all_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_shifts = all_shifts_get(db, skip=skip, limit=limit)
    return all_shifts

@router.post("/", response_model=ShiftOut, status_code=status.HTTP_201_CREATED)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    created_shift = shift_create(db, shift)
    
    if not created_shift:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong creating the shift")
    
    return create_shift

@router.patch("/{shift_id}", response_model=ShiftOut)
def update_shift(shift_id: int, shift: ShiftUpdate, db: Session = Depends(get_db)):
    updated_shift = shift_update(db, shift_id, shift)
    if not updated_shift:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wr")