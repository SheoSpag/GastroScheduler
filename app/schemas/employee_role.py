from pydantic import BaseModel
from app.schemas.employee import EmployeeOut
from app.schemas.role import RoleOut

class EmployeeRoleOut(BaseModel):
    employee: EmployeeOut
    role: RoleOut