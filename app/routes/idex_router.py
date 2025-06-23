from fastapi import APIRouter

from app.routes.company_routes import router as company_router
from app.routes.branch_routes import router as branch_router

router = APIRouter()

router.include_router(company_router, prefix="/company", tags=["companies"])
router.include_router(branch_router, prefix="/branch", tags=["branches"])