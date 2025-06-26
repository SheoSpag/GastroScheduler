from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeUpdate, EmployeeCreate

def get_employee(db: Session, employee_id: int):
    from app.models.employee import Employee
    
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_all_employees(db: Session,  skip: int = 0, limit: int = 100):
    from app.models.employee import Employee
    
    return db.query(Employee).offset(skip).limit(limit).all()

def get_employee_locks(db: Session, employee_id: int):
    from app.models.lock import Lock
    
    return db.query(Lock).filter(Lock.employee_id == employee_id).all()

def create_employee(db: Session, employee: EmployeeCreate):
    from app.models.employee import Employee
    
    created_employee = Employee(name=employee.name, hourly_wage=employee.hourly_wage, monthly_hours=employee.monthly_hours, branch_id=employee.branch_id)
    
    db.add(created_employee)
    db.commit()
    db.refresh(created_employee)
    
    return created_employee

def update_employee(db:Session, employee_id: int, employee: EmployeeUpdate):
    searched_employee = get_employee(db, employee_id)
    if not searched_employee:
        return None
    
    update_date = employee.model_dump(exclude_unset=True)
    
    for key, value in update_date.items():
        setattr(searched_employee, key, value)
        
    db.commit()
    db.refresh(searched_employee)
    return searched_employee

def delete_employee(db: Session, employee_id):
    searched_employee = get_employee(db, employee_id)
    
    if not searched_employee:
        return None
    
    db.delete(searched_employee)
    db.commit()
    
    return searched_employee
    