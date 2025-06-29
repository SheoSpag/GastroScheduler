from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str
    area_id: int
    
class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name : Optional[str] = None
    
class RoleOut(RoleBase):
    id: int 
    
    model_config = {"from_attributes": True}
    