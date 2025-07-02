from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.schemas.role import RoleOut
from app.schemas.employee_role import EmployeeRoleOut
from app.schemas.lock import LockOut
from app.crud.employee import get_employee as employee_get, delete_employee as employee_delete, update_employee as employee_update, get_all_employees as all_employees_get, create_employee as employee_create, get_employee_locks as employee_locks_get, asign_employee_role as employee_role_asign, get_employee_roles as employee_roles_get

router = APIRouter()

@router.get("/{employee_id}", response_model=EmployeeOut, status_code=status.HTTP_200_OK)
def get_all_employees(employee_id: int, db: Session = Depends(get_db)):
        return employee_get(db, employee_id)

@router.get("/", response_model=List[EmployeeOut], status_code=status.HTTP_200_OK)
def get_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_employees = all_employees_get(db, skip=skip, limit=limit)
    
    if not all_employees:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return all_employees

@router.get("/lock/{employee_id}", response_model=List[LockOut], status_code=status.HTTP_200_OK)
def get_employee_locks(employee_id: int, db: Session = Depends(get_db)):
    searched_locks = employee_locks_get(db, employee_id)
    
    if not searched_locks: 
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return searched_locks

@router.get("/{employee_id}/roles", response_model=List[RoleOut], status_code=status.HTTP_200_OK)
def get_employee_roles(employee_id: int, db: Session = Depends(get_db)):
    
    employee_roles = employee_roles_get(db, employee_id)
    
    if not employee_roles:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return employee_roles
    

@router.post("/", response_model=EmployeeCreate, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):    
    return employee_create(db, employee)


@router.post("/{employee_id}/role/{role_id}", response_model=EmployeeRoleOut, status_code=status.HTTP_201_CREATED)
def asign_employee_role(employee_id: int, role_id: int, db: Session = Depends(get_db)):
    employee, role = employee_role_asign(db, employee_id, role_id)
    return EmployeeRoleOut(employee=employee, role=role)



@router.patch("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    return employee_update(db, employee_id, employee)

@router.delete("/{employee_id}", response_model=EmployeeOut)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_delete(db, employee_id)

    