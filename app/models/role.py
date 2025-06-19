from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from employee_role import employee_role

Base = declarative_base()

class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    area = relationship("Area", back_populates="roles")
    
    employees = relationship("Employee", secondary=employee_role, back_populates="roles")