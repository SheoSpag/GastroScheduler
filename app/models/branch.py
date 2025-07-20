from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Branch(Base):
    __tablename__ = "branch"
    
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    
    company_id = Column(Integer, ForeignKey('company.id', ondelete="CASCADE"), nullable=False)
    company = relationship("Company", back_populates="branches")
    
    employees = relationship("Employee", back_populates="branch", cascade="all, delete-orphan")
    
    days_settings = relationship("DaySettings", back_populates="branch", cascade="all, delete-orphan")
    
    areas = relationship("Area", back_populates="branch", cascade="all, delete-orphan")

    managers = relationship("BranchManager", back_populates="branch")


    
