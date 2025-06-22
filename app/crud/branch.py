from sqlalchemy.orm import Session
from app.schemas.branch import BranchCreate, BranchUpdate

def get_branch(db: Session, branch_id: int):
    from app.models.branch import Branch
    
    return db.query(Branch).filter(Branch.id == branch_id).first()

def get_branches(db: Session, skip: int = 0, limit: int = 100):
    from app.models.branch import Branch
    
    return db.query(Branch).offset(skip).limit(limit).all()

def create_branch(db: Session, branch: BranchCreate):
    from app.models.branch import Branch
    
    created_branch = Branch(address=branch.address, opening=branch.opening, closing=branch.closing, company_id=branch.company_id)
    
    db.add(create_branch)
    db.commit()
    db.refresh(create_branch)
    
    return created_branch

def update_branch(db: Session, branch_id: int, branch : BranchUpdate):
    searched_branch = get_branch(db, branch_id)
    if not searched_branch:
        return None
    
    update_data = branch.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(searched_branch, key, value)
        
    db.commit()
    db.refresh(searched_branch)
    return searched_branch

def delete_branch(db: Session, branch_id: int):
    searched_branch = get_branch(db, branch_id)
    
    if not searched_branch:
        return None
    
    db.delete(searched_branch)
    db.commit()
    
    return searched_branch
    
    