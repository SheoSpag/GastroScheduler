from sqlalchemy import Column, Integer, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Branch(Base):
    __tablename__ = "branch"
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    opening = Column(Time, nullable=False)
    closing = Column(Time, nullable=False)
    
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    company = relationship("Company", back_populates="branch")
    
    employees = relationship("Employee", back_populates="branch")
    
