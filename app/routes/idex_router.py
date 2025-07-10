from fastapi import APIRouter

from app.routes.company_routes import router as company_router
from app.routes.branch_routes import router as branch_router
from app.routes.day_settings_routes import router as day_settings_router
from app.routes.employee_routes import router as employee_router
from app.routes.lock_routes import router as lock_router
from app.routes.area_routes import router as area_router
from app.routes.role_routes import router as role_router
from app.routes.shift_routes import router as shift_router
from app.routes.ai_router import router as ia_router

router = APIRouter()

router.include_router(company_router, prefix="/company", tags=["companies"])
router.include_router(branch_router, prefix="/branch", tags=["branches"])
router.include_router(day_settings_router, prefix="/branch/{branch_id}/settings", tags=["day_settings"])
router.include_router(employee_router, prefix="/employee", tags=["employees"])
router.include_router(lock_router, prefix="/lock", tags=["locks"])
router.include_router(area_router, prefix="/area", tags=["areas"])
router.include_router(role_router, prefix="/role", tags=["roles"])  
router.include_router(shift_router, prefix="/shift", tags=["shifts"])  
router.include_router(ia_router, prefix="/ia", tags=["ia"])