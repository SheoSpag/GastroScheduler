from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.branch import BranchCreate, BranchOut, BranchUpdate
from app.crud.branch import get_branch as branch_get, get_branches as branches_get, create_branch as branch_create, update_branch as branch_update, delete_branch as branch_delete

router = APIRouter()

@router.post("/", response_model=BranchCreate, status_code=status.HTTP_201_CREATED)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    db_branch = branch_create(db, branch)
    return db_branch

@router.get("/{branch_id}", response_model=BranchOut, status_code=status.HTTP_200_OK)
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = get_branch(db, branch_id)
    return db_branch

@router.get("/", response_model=List[BranchOut])
def get_branches(skip: int = 0, limit: int = 100, db : Session = Depends(get_db)):
    db_branches = get_branches(db, skip=skip, limit=limit)
    return db_branches

@router.patch("/{branch_id}", response_model=BranchOut)
def update_branch(branch_id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    updated_branch = branch_update(db, branch_id, branch)
    if not updated_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return update_branch

@router.delete("/{branch_id}", response_model=BranchOut)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    deleted_branch = branch_delete(db, branch_id)
    if not deleted_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return deleted_branch
    