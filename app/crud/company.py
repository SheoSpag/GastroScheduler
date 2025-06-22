from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate

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
