from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate, CompanyUpdate
from fastapi import status
from app.exceptions.customError import CustomError
from app.utils.error_handler import handle_exception

def get_company(db: Session, company_id: int):
    from app.models.company import Company
    searched_company = db.query(Company).filter(Company.id == company_id).first()
    
    if not searched_company:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    
    return searched_company

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    from app.models.company import Company

    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company : CompanyCreate):
    from app.models.company import Company
    
    try:
        created_company = Company(name=company.name)
    
        db.add(created_company)
        db.commit()
        db.refresh(created_company)
        
    
        return created_company
    except Exception as e:
        db.rollback()
        handle_exception(e, "Interal error creating the company")

def update_company(db: Session, company_id: int, company: CompanyUpdate):
    try:
        searched_company = get_company(db, company_id)
    
        searched_company.name = company.name
    
        db.commit()
        db.refresh(searched_company)
    
        return searched_company
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the company")

def delete_company(db: Session, company_id: int):
    try:
        searched_company = get_company(db, company_id)
    
    
        db.delete(searched_company)
        db.commit()
    
        return searched_company
    
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error deleting the company")
    
        
