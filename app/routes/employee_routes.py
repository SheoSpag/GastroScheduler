from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.schemas.lock import LockOut
from app.crud.employee import get_employee as employee_get, delete_employee as employee_delete, update_employee as employee_update, get_all_employees as all_employees_get, create_employee as employee_create, get_employee_locks as employee_locks_get
from app.crud.branch import get_branch

router = APIRouter()

@router.get("/{employee_id}", response_model=EmployeeOut, status_code=status.HTTP_200_OK)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
        searched_employee = employee_get(db, employee_id)
        if not searched_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return searched_employee

@router.get("/", response_model=List[EmployeeOut], status_code=status.HTTP_200_OK)
def get_employee(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_employees = all_employees_get(db, skip=skip, limit=limit)
    return all_employees

@router.get("/lock/{employee_id}", response_model=List[LockOut], status_code=status.HTTP_200_OK)
def get_employee_locks(employee_id: int, db: Session = Depends(get_db)):
    searched_locks = employee_locks_get(db, employee_id)
    if not searched_locks: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return searched_locks

@router.post("/", response_model=EmployeeCreate, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    searched_branch = get_branch(db, employee.branch_id)
    if not searched_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    created_employee = employee_create(db, employee)
    return created_employee

@router.patch("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    updated_employee = employee_update(db, employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

@router.delete("/{employee_id}", response_model=EmployeeOut)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted_employee = employee_delete(db, employee_id)
    if not delete_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return deleted_employee
    

    