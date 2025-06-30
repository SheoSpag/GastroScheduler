from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class ShiftBase(BaseModel):
    start_date_time: datetime
    end_date_time: datetime
    date: date
    role_id: int
    employee_id: int
    
class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    start_date_time: Optional[datetime] = None
    end_date_time: Optional[datetime] = None
    role_id: Optional[int] = None
    employee_id: Optional[int] = None
    
class ShiftOut(ShiftBase):
    id: int
    
    model_config = {"from_attributes": True}
    
