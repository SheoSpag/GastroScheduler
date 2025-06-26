from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.lock import LockCreate, LockUpdate, LockOut
from app.crud.lock import get_lock as lock_get, get_all_locks as all_locks_get, create_lock as lock_create, delete_lock as lock_delete, update_lock as lock_update
from app.crud.employee import get_employee

router = APIRouter()

@router.post("/", response_model=LockOut, status_code=status.HTTP_201_CREATED)
def create_lock(lock: LockCreate, db: Session = Depends(get_db)):
    searched_employee = get_employee(db, lock.employee_id)
    if not searched_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    created_lock = lock_create(db, lock)
    return created_lock

@router.get("/{lock_id}", response_model=LockOut, status_code=status.HTTP_200_OK)
def get_lock(lock_id: int, db: Session = Depends(get_db)):
    searched_lock = lock_get(db, lock_id)
    if not searched_lock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lock not found")
    return searched_lock

@router.get("/", response_model=List[LockOut], status_code=status.HTTP_200_OK)
def get_all_locks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_locks = all_locks_get(db, skip=skip, limit=limit)
    return all_locks_get

@router.patch("/{lock_id}", response_model=LockOut)
def update_lock(lock_id: int, lock: LockUpdate, db: Session = Depends(get_db)):
    updated_lock = lock_update(db, lock_id, lock)
    if not updated_lock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lock not found")
    return updated_lock
    
@router.delete("/{lock_id}", response_model=LockOut, status_code=status.HTTP_200_OK)
def delete_lock(lock_id: int, db: Session = Depends(get_db)):
    deleted_lock = lock_delete(db, lock_id)
    if not deleted_lock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lock not found")
    return deleted_lock

    