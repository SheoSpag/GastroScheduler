from pydantic import BaseModel, constr
from typing import Optional, Annotated

class BranchBase(BaseModel):
    address: Annotated[str, constr(min_length=3, max_length=255)]
    company_id: int
    
class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    address: Optional[Annotated[str, constr(min_length=3, max_length=255)]] = None
    company_id: Optional[int] = None
    
class BranchOut(BranchBase):
    id: int

    class Config:
        orm_mode = True 