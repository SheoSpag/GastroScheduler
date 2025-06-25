from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    hourly_wage: float
    monthly_hours: int
    branch_id: int
    
class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    hourly_wage: Optional[float] = None
    monthly_hours: Optional[int] = None
    branch_id: Optional[int] = None

class EmployeeOut(EmployeeBase):
    id: int
    
    class Config:
        orm_mode = True