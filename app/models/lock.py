from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from enum import Enum 

from lock_status import LockStatus

Base = declarative_base()

class Lock(Base):
    __tablename__ = "lock"
    date = Column(DateTime, nullable=False)
    note = Column(String, nullable=True)
    status = Column(Enum(LockStatus), nullable=False)
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    employee = relationship("Employee", back_populates="lock")