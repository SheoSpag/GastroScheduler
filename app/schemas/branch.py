from pydantic import BaseModel, constr
from datetime import time
from typing import Optional, Annotated

class BranchBase(BaseModel):
    address: Annotated[str, constr(min_length=3, max_length=255)]
    opening: time
    closing: time
    company_id: int
    
class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    address: Optional[Annotated[str, constr(min_length=3, max_length=255)]] = None
    opening: Optional[time] = None
    closing: Optional[time] = None
    company_id: Optional[int] = None
    
class BranchOut(BranchBase):
    id: int

    class Config:
        orm_mode = True 