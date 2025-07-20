from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.branch_manager import BranchManagerCreate, BranchManagerOut
from app.crud.branch_manager import create_branch_manager
from app.db.db import get_db
from app.schemas.branch_manager import BranchManagerCreate, BranchManagerOut
from app.models.branch_manager import BranchManager

router = APIRouter()

@router.post("/register", response_model=BranchManagerOut, status_code=status.HTTP_201_CREATED)
def register_branch_manager( branch_manager_in: BranchManagerCreate, db: Session = Depends(get_db)):
    return create_branch_manager(db, email=branch_manager_in.email, password=branch_manager_in.password, branch_id=branch_manager_in.branch_id)
