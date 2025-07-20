from pydantic import BaseModel, EmailStr

class BranchManagerBase(BaseModel):
    email: EmailStr
    branch_id: int

class BranchManagerCreate(BranchManagerBase):
    password: str 

class BranchManagerOut(BranchManagerBase):
    id: int

    model_config = {"from_attributes": True} 
