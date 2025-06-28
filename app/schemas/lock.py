from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, timezone  
from app.models.lock_reason import LockReason

class LockCBase(BaseModel):
    created_date: Optional[datetime] = datetime.now(timezone.utc)
    note: Optional[str] = None
    locked_date: date
    lock_reason: Optional[LockReason] = LockReason.WISH
    employee_id: int
    
class LockCreate(LockCBase):
    pass

class LockUpdate(BaseModel):
    note: Optional[str] = None
    locked_date: Optional[date] = None
    lock_reason: Optional[LockReason] = None
    
class LockOut(LockCBase):
    id: int
    
    model_config = {"from_attributes": True} 
