from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import time
from app.db.db import Base

class DaySettings(Base):
    __tablename__ = "day_setting"

    week_day = Column(Integer, nullable=False)
    morning_intensity = Column(Integer, default=0)
    afternoon_intensity = Column(Integer, default=0)
    evening_intensity = Column(Integer, default=0)
    opening = Column(Time, nullable=False)
    closing = Column(Time, nullable=False)
    
    branch_id = Column(Integer, ForeignKey("branch.id", ondelete="CASCADE"), nullable=False)
    branch = relationship("Branch", back_populates="days_settings")
    
    __table_args__ = (
        PrimaryKeyConstraint('branch_id', 'week_day'),
    )