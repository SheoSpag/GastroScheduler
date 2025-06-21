from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.crud.company import get_company, get_companies, create_company, update_company, delete_company

router = APIRouter()