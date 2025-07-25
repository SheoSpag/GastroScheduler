from fastapi import APIRouter, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.branch_manager import BranchManagerCreate, BranchManagerOut
from app.crud.branch_manager import create_branch_manager, authenticate_branch_manager, verify_email as email_verify
from app.db.db import get_db
from app.schemas.branch_manager import BranchManagerCreate, BranchManagerOut
from app.schemas.token import Token
from app.auth.jwt_auth import create_access_token, verify_email_token


router = APIRouter()

@router.post("/register", response_model=BranchManagerOut, status_code=status.HTTP_201_CREATED)
def register_branch_manager( branch_manager_in: BranchManagerCreate, db: Session = Depends(get_db)):
    return create_branch_manager(db, email=branch_manager_in.email, password=branch_manager_in.password, branch_id=branch_manager_in.branch_id)

@router.get("/verify", status_code=status.HTTP_200_OK)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    
    email = verify_email_token(token)
    
    return email_verify(db, email)
    
        

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_branch_manager(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    manager = authenticate_branch_manager(db, form_data.username, form_data.password)
    
    
    token = create_access_token(data={"sub": manager.email})
     
    return {"access_token": token, "token_type": "bearer"}
    