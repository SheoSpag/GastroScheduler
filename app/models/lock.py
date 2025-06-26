from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.db import Base

from app.models.lock_reason import LockReason


class Lock(Base):
    __tablename__ = "lock"
    id = Column(Integer, primary_key=True)
    locked_date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    lock_reason = Column(SQLEnum(LockReason), default=LockReason.WISH)
    created_at = Column(DateTime, default=datetime.now)
    
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"), nullable=False)    
    employee = relationship("Employee", back_populates="locks")
    
    
    __table_args__ = (
        UniqueConstraint("employee_id", "locked_date"),
    )