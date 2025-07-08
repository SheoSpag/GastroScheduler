from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.branch import BranchCreate, BranchOut, BranchUpdate
from app.schemas.employee import EmployeeOut
from app.schemas.lock import LockOut
from app.schemas.area import AreaOut
from app.crud.branch import get_branch as branch_get, get_branches as branches_get, create_branch as branch_create, update_branch as branch_update, delete_branch as branch_delete, get_branch_employees as branch_employees_get, get_branch_locks as branch_locks_get, get_branch_areas as branch_areas_get

router = APIRouter()

@router.post("/", response_model=BranchOut, status_code=status.HTTP_201_CREATED)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return branch_create(db, branch)
    
@router.get("/{branch_id}", response_model=BranchOut, status_code=status.HTTP_200_OK)
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    return branch_get(db, branch_id)

@router.get("/{branch_id}/employees", response_model=List[EmployeeOut], status_code=status.HTTP_200_OK)
def get_branch_employees(branch_id: int, skip: int = 0, limit: int = 100, db : Session = Depends(get_db)):
    searched_employees = branch_employees_get(db ,branch_id, skip=skip, limit=limit)
    if not searched_employees:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return searched_employees

@router.get("/", response_model=List[BranchOut])
def get_branches(skip: int = 0, limit: int = 100, db : Session = Depends(get_db)):
    all_branches = branches_get(db, skip=skip, limit=limit)
    if not all_branches:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return all_branches

@router.get("/{branch_id}/locks", response_model=List[LockOut], status_code=status.HTTP_200_OK)
def get_branch_locks(branch_id: int, db: Session = Depends(get_db)):
    searched_locks = branch_locks_get(db, branch_id)
    if not searched_locks:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return searched_locks

@router.get("/{branch_id}/areas", response_model=List[AreaOut], status_code=status.HTTP_200_OK)
def get_branch_areas(branch_id: int, db: Session = Depends(get_db)):
    branch_areas = branch_areas_get(db, branch_id)
    if not branch_areas:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return branch_areas

@router.patch("/{branch_id}", response_model=BranchOut, status_code=status.HTTP_200_OK)
def update_branch(branch_id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    return branch_update(db, branch_id, branch)
    
@router.delete("/{branch_id}", response_model=BranchOut)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    return branch_delete(db, branch_id)
    