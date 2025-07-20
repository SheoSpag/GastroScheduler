from sqlalchemy.orm import Session
from fastapi import status
from app.models.branch_manager import BranchManager
from app.auth.security import hash_password
from app.utils.error_handler import CustomError
from app.crud.branch import get_branch

def get_branch_manager_by_email(db: Session, branch_manager_email: str):
    from app.models.branch_manager import BranchManager
    
    return db.query(BranchManager).filter(BranchManager.email == branch_manager_email).first()

def create_branch_manager(db: Session, email: str, password: str, branch_id: int) -> BranchManager:
    from app.models.branch_manager import BranchManager
    
    if get_branch_manager_by_email(db, email):
        raise CustomError(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    if get_branch(db, branch_id) is None:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    
    
    hashed_pw = hash_password(password)
    db_branch_manager = BranchManager(email=email, hashed_password=hashed_pw, branch_id=branch_id)
    db.add(db_branch_manager)
    db.commit()
    db.refresh(db_branch_manager)
    return db_branch_manager


