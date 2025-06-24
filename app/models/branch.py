from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Branch(Base):
    __tablename__ = "branch"
    
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    company = relationship("Company", back_populates="branches")
    
    employees = relationship("Employee", back_populates="branch")
    
    days_settings = relationship("DaySettings", back_populates="branch")

    
