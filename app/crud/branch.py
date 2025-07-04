from sqlalchemy.orm import Session
from app.schemas.branch import BranchCreate, BranchUpdate
from fastapi import status
from app.exceptions.customError import CustomError
from app.crud.company import get_company
from app.utils.error_handler import handle_exception
from datetime import time

def get_branch(db: Session, branch_id: int):
    from app.models.branch import Branch
    searched_branch = db.query(Branch).filter(Branch.id == branch_id).first()
    
    if not searched_branch:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    
    return searched_branch

def get_branches(db: Session, skip: int = 0, limit: int = 100):
    from app.models.branch import Branch
    
    return db.query(Branch).offset(skip).limit(limit).all()

def get_branch_employees(db: Session, branch_id: int,  skip: int = 0, limit: int = 100):
    from app.models.employee import Employee
    
    #Only 4 validation
    get_branch(db, branch_id)
    
    return db.query(Employee).filter(Employee.branch_id == branch_id).offset(skip).limit(limit).all()

def get_branch_locks(db: Session, branch_id: int):
    from app.models.lock import Lock
    from app.models.employee import Employee
    
    #Only 4 validation
    get_branch(db, branch_id)
    
    return db.query(Lock).join(Employee).filter(Employee.branch_id == branch_id).all()

def get_branch_areas(db: Session, branch_id: int):
    from app.models.area import Area 
    
    #Just 4 validation
    get_branch(db, branch_id)
    return db.query(Area).filter(Area.branch_id == branch_id).all()

def create_branch(db: Session, branch: BranchCreate):
    from app.models.branch import Branch
    from app.models.day_settings import DaySettings
    
    try:
        #Just For Validation
        get_company(db, branch.company_id)
        
        created_branch = Branch(address=branch.address, company_id=branch.company_id)
        
        db.add(created_branch)
        db.commit()
        db.refresh(created_branch)
        
        for day in range(7):
            base_intensity = DaySettings(week_day=day, morning_intensity = 0, afternoon_intensity=0, evening_intensity=0, opening=time(0,0,0), closing=time(0,0,0), branch_id=created_branch.id)
            db.add(base_intensity)
        
        db.commit()
        
        return created_branch
    except Exception as e:
        db.rollback()
        handle_exception(e, "Interal error creating de branch")

def update_branch(db: Session, branch_id: int, branch : BranchUpdate):
    try:
        searched_branch = get_branch(db, branch_id)
        
        update_data = branch.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(searched_branch, key, value)
            
        #Just 4 validation   
        if "company_id" in update_data:
            get_company(db, update_data["company_id"])
        
        db.commit()
        db.refresh(searched_branch)
        return searched_branch
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the branch")

def delete_branch(db: Session, branch_id: int):
    try:
        searched_branch = get_branch(db, branch_id)
        
        db.delete(searched_branch)
        db.commit()
        
        return searched_branch
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error deleting the company")
    
    