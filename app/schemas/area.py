from pydantic import BaseModel
from typing import Optional
from datetime import time

class AreaBase(BaseModel):
    opening_time: time
    closing_time: time
    minimum_staff: int
    maximum_staff: int
    name: str
    branch_id: int
    
class AreaCreate(AreaBase):
    pass 

class AreaUpdate(BaseModel):
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    minimum_staff: Optional[int] = None
    maximum_staff: Optional[int] = None
    name: Optional[str] = None
    
class AreaOut(AreaBase):
    id: int 
    
    model_config = {"from_attributes": True}