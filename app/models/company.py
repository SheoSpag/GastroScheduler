from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.db import Base

class Company(Base): 
    __tablename__ = 'company'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    branches = relationship("Branch", back_populates="company")