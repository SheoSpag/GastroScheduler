from pydantic import BaseModel, constr
from typing import Optional

class IntensityBase(BaseModel):
    week_day: int
    morning_intensity: int 
    afternoon_intensity: int 
    evening_intensity: int 
    branch_id: int
    
class IntensityCreate(IntensityBase):
    pass 

class IntensityUpdate(BaseModel):
    morning_intensity: Optional[int] = None
    afternoon_intensity: Optional[int] = None
    evening_intensity: Optional[int] = None 
    
class IntensityOut(IntensityBase):
    id: int
    
    class Config:
        orm_mode = True