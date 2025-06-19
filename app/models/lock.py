from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from enum import Enum 

from lock_reason import LockReason

Base = declarative_base()

class Lock(Base):
    __tablename__ = "lock"
    
    locked_date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    reason = Column(Enum(LockReason), default=LockReason.WISH)
    created_at = Column(DateTime, default=datetime.now)
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)    
    employee = relationship("Employee", back_populates="locks")
    
    
    __table_args__ = (
        PrimaryKeyConstraint('employee_id', 'locked_date'),
    )