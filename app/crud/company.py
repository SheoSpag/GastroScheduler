from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate

def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company : CompanyCreate):
    created_company = Company(name=company.name)
    db.add(create_company)
    db.commit()
    db.refresh(create_company)
    return created_company

def update_company(db: Session, company_id: int, company: CompanyUpdate):
    serched_company = get_company(db, company_id)
    if not serched_company:
        return None
    serched_company.name = company.name
    db.commit()
    db.refresh(serched_company)
    return serched_company

def delete_company(db: Session, company_id: int):
    serched_company = get_company(db, company_id)
    if not serched_company:
        return None
    db.delete(serched_company)
    db.commit()
    return serched_company
