from sqlalchemy import Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Emlpoyee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hourly_wage = Column(Float, nullable=True)
    monthly_hours = Column(Integer, nullable=False)
    
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    branch = relationship("Branch", back_populates="employee")
    