from fastapi import APIRouter

from app.routes.company_routes import router as company_router

router = APIRouter()

router.include_router(company_router, prefix="/companies", tags=["companies"])