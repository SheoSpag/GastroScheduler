from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.schemas.employee import EmployeeOut
from app.crud.role import get_role as role_get, get_roles as roles_get, create_role as role_create, update_role as role_update, deleted_role as role_delete, get_role_employees as role_employees_get

router = APIRouter()

@router.get("/", response_model=List[RoleOut], status_code=status.HTTP_200_OK)
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_roles = roles_get(db, skip=skip, limit=limit)
    return all_roles

@router.get("/{role_id}", response_model=RoleOut, status_code=status.HTTP_200_OK)
def get_role(role_id: int, db: Session = Depends(get_db)):
    searched_role = role_get(db, role_id)
    
    if not searched_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    return searched_role

@router.get("/{role_id}/employees", response_model=List[EmployeeOut], status_code=status.HTTP_200_OK)
def get_role_employees(role_id: int, db: Session = Depends(get_db)):
    role_employees = role_employees_get(db, role_id)
    
    if not role_employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    return role_employees

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    created_role = role_create(db, role)
    if not created_role:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong while creating the role")
    return created_role

@router.patch("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    updated_role = role_update(db, role_id, role)
    if not updated_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return updated_role

@router.delete("/{role_id}", response_model=RoleOut)
def delete_role(role_id:int, db: Session = Depends(get_db)):
    deleted_role = role_delete(db, role_id)
    if not deleted_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return deleted_role
    
    