from sqlalchemy.orm import Session
from fastapi import status
from app.models.branch_manager import BranchManager
from app.auth.security import hash_password, verify_password
from app.auth.jwt_auth import create_email_verification_token
from app.auth.email_verification import send_verification_email
from app.utils.error_handler import CustomError
from app.crud.branch import get_branch
from app.utils.error_handler import handle_exception

def get_branch_manager_by_email(db: Session, branch_manager_email: str):
    from app.models.branch_manager import BranchManager
    
    return db.query(BranchManager).filter(BranchManager.email == branch_manager_email).first()

def authenticate_branch_manager(db: Session, email: str, password: str):

    searched_branch_manager = get_branch_manager_by_email(db, email)
    
    if not searched_branch_manager:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Branch manager not found")
        
    if not verify_password(password, searched_branch_manager.hashed_password):
        raise CustomError(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return searched_branch_manager
    


def create_branch_manager(db: Session, email: str, password: str, branch_id: int):
    from app.models.branch_manager import BranchManager
    
    try:
        existing_manager = get_branch_manager_by_email(db, email)

        if existing_manager:
            raise CustomError(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        #Just 4 validation
        get_branch(db, branch_id)
        print("Antes del hash")
        hashed_pw = hash_password(password)
        db_branch_manager = BranchManager(email=email, hashed_password=hashed_pw, branch_id=branch_id)
        db.add(db_branch_manager)
        
        
        print("Antes del token")
        token = create_email_verification_token(email)
        print(f"Token creado cheto {token}")
        verification_link = f"http://localhost:8000/branch_manager/verify?token={token}"
        
        send_verification_email(to_email=email, verification_link=verification_link)
        
        db.commit()
        db.refresh(db_branch_manager)
        
        return db_branch_manager
    except Exception as e:
        db.rollback()
        handle_exception(e, "Interal error creating de branch")



def verify_email(db: Session, email: str):
    try:
        user = get_branch_manager_by_email(db, email)
        
        if user.is_verified:
            return { "email": "Email already verified"}
        
        user.is_verified = True
        db.commit()
        
        return { "email": "Email verified"}
    except Exception as e:
        db.rollback()
        handle_exception(e, "Interal error creating de branch")