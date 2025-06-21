from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey 
from sqlalchemy.orm import relationship
from app.db.db import Base

class Shift(Base):
    __tablename__ = "shift"
    
    id = Column(Integer, primary_key=True)
    start_date_time = Column(DateTime, nullable=False)
    end_date_time = Column(DateTime, nullable=False)
    date = Column(Date, nullable=False)
    
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    role = relationship("Role") # USAR JOINEDLOAD PARA CONSULTAS CON SESSION.QUERY
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    employee = relationship("Employee", back_populates="shifts")
    