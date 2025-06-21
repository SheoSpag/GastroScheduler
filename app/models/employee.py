from sqlalchemy import Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

from app.models.employee_role import employee_role


class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hourly_wage = Column(Float, nullable=True)
    monthly_hours = Column(Integer, nullable=False)
    
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    branch = relationship("Branch", back_populates="employees")
    
    locks = relationship("Lock", back_populates="employee")
    
    shifts = relationship("Shift", back_populates="employee")
    
    roles = relationship("Role", secondary=employee_role, back_populates="employees")