from sqlalchemy import Column, Integer, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Area(Base):
    __tablename__ = "area"
    
    id = Column(Integer, primary_key=True)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    minimum_staff = Column(Integer, default=1)
    maximum_staff = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    
    branch_id = Column(Integer, ForeignKey("branch.id", ondelete="CASCADE"), nullable=False)
    branch = relationship("Branch", back_populates="areas")

    
    roles = relationship("Role", back_populates="area", cascade="all, delete-orphan")