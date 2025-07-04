from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.crud.company import get_company as company_get, get_companies as companies_get, create_company as company_create, update_company as company_update, delete_company as company_delete

router = APIRouter()

@router.post("/", response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return company_create(db, company)

@router.get("/{company_id}", response_model=CompanyOut, status_code=status.HTTP_200_OK)
def get_company(company_id: int, db: Session = Depends(get_db)):
    return  company_get(db, company_id)

@router.get("/", response_model=List[CompanyOut], status_code=status.HTTP_200_OK)
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_companies = companies_get(db, skip=skip, limit=limit)
    if not all_companies:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return all_companies

@router.put("/{company_id}", response_model=CompanyOut, status_code=status.HTTP_200_OK)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    return company_update(db, company_id, company)

@router.delete("/{company_id}", response_model=CompanyOut, status_code=status.HTTP_200_OK)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    return company_delete(db, company_id)
    