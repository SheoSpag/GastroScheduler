from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.db.db import Base

class BaseIntensity(Base):
    __tablename__ = "base_intensity"

    week_day = Column(Integer, nullable=False)
    morning_intensity = Column(Integer, default=0)
    afternoon_intensity = Column(Integer, default=0)
    evening_intensity = Column(Integer, default=0)
    
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    branch = relationship("Branch", back_populates="regular_intensities")
    
    __table_args__ = (
        PrimaryKeyConstraint('branch_id', 'week_day'),
    )