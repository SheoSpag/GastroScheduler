from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey, PrimaryKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.db import Base

from app.models.lock_reason import LockReason


class Lock(Base):
    __tablename__ = "lock"
    
    locked_date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    reason = Column(SQLEnum(LockReason), default=LockReason.WISH)
    created_at = Column(DateTime, default=datetime.now)
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)    
    employee = relationship("Employee", back_populates="locks")
    
    
    __table_args__ = (
        PrimaryKeyConstraint('employee_id', 'locked_date'),
    )