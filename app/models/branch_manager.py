
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.db import Base

class BranchManager(Base):
    __tablename__ = "branch_managers"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    branch_id = Column(Integer, ForeignKey("branch.id"), nullable=False)
    is_verified = Column(Boolean, default=False)
    
    branch = relationship("Branch", back_populates="managers")
