from db import Base, engine

from ..models import area, base_intensity, branch, company, employee_role, employee, lock_reason, lock, role, shift

def init_db():
    print("Creating tables in the database..")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")
    
if __name__ == "__main__":
    init_db()