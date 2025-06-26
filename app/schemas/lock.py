from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, timezone  
from app.models.lock_reason import LockReason

class LockCBase(BaseModel):
    created_date: Optional[datetime] = datetime.now(timezone.utc)
    note: Optional[str] = None
    locked_date: date
    lock_reason: LockReason
    employee_id: int
    
class LockCreate(LockCBase):
    pass

class LockUpdate(BaseModel):
    note: Optional[str]
    locked_date: Optional[date]
    lock_reason: Optional[LockReason]
    
class LockOut(LockCBase):
    id: int
    
    class Config:
        orm_mode = True    
