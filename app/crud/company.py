from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate, CompanyUpdate

def get_company(db: Session, company_id: int):
    from app.models.company import Company
    
    return db.query(Company).filter(Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    from app.models.company import Company
    
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company : CompanyCreate):
    from app.models.company import Company
    
    created_company = Company(name=company.name)
    
    db.add(created_company)
    db.commit()
    db.refresh(created_company)
    
    return created_company

def update_company(db: Session, company_id: int, company: CompanyUpdate):
    searched_company = get_company(db, company_id)
    
    if not searched_company:
        return None
    
    searched_company.name = company.name
    
    db.commit()
    db.refresh(searched_company)
    
    return searched_company

def delete_company(db: Session, company_id: int):
    searched_company = get_company(db, company_id)
    
    if not searched_company:
        return None
    
    db.delete(searched_company)
    db.commit()
    
    return searched_company
