from pydantic import BaseModel
from datetime import time
from typing import Optional

class SettingsBase(BaseModel):
    week_day: int
    morning_intensity: int 
    afternoon_intensity: int 
    evening_intensity: int 
    opening: time
    closing: time
    branch_id: int
    
class SettingsCreate(SettingsBase):
    pass 

class SettingsUpdate(BaseModel):
    morning_intensity: Optional[int] = None
    afternoon_intensity: Optional[int] = None
    evening_intensity: Optional[int] = None 
    opening: Optional[time] = None 
    closing: Optional[time] = None 
    
class SettingsOut(SettingsBase):
    
    model_config = {"from_attributes": True}