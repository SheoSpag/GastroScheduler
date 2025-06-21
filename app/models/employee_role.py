from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.db import Base

employee_role = Table(
    "employee_role",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)
