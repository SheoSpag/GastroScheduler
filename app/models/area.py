from sqlalchemy import Column, Integer, Time, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.db.db import Base

class Area(Base):
    __tablename__ = "area"
    
    id = Column(Integer, primary_key=True)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    minimum_staff = Column(Integer, default=1)
    maximum_staff = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    
    roles = relationship("Role", back_populates="area")