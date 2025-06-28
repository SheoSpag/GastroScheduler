from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    
class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass 

class CompanyOut(CompanyBase):
    id: int
    
    model_config = {"from_attributes": True}
