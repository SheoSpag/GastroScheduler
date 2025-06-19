from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shift(Base):
    id = Column(Integer, primary_key=True)
    date_time_start = Column(DateTime, nullable=False)
    date_time_end = Column(DateTime, nullable=False)
    date = Column(Date, nullable=False)
    
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    role = relationship("Role") # USAR JOINEDLOAD PARA CONSULTAS CON SESSION.QUERY
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    employee = relationship("Employee", back_populates="shifts")
    