from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.schemas.employee import EmployeeOut
from app.crud.role import get_role as role_get, get_roles as roles_get, create_role as role_create, update_role as role_update, delete_role as role_delete, get_role_employees as role_employees_get

router = APIRouter()

@router.get("/", response_model=List[RoleOut], status_code=status.HTTP_200_OK)
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_roles = roles_get(db, skip=skip, limit=limit)
    
    if not all_roles:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return all_roles

@router.get("/{role_id}", response_model=RoleOut, status_code=status.HTTP_200_OK)
def get_role(role_id: int, db: Session = Depends(get_db)):
    return role_get(db, role_id)

@router.get("/{role_id}/employees", response_model=List[EmployeeOut], status_code=status.HTTP_200_OK)
def get_role_employees(role_id: int, db: Session = Depends(get_db)):
    role_employees = role_employees_get(db, role_id)
    
    if not role_employees:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return role_employees

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_create(db, role)

@router.patch("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return role_update(db, role_id, role)

@router.delete("/{role_id}", response_model=RoleOut)
def delete_role(role_id:int, db: Session = Depends(get_db)):
    return role_delete(db, role_id)
    
    