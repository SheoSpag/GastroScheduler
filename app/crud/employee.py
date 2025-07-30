from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeUpdate, EmployeeCreate
from fastapi import status
from app.crud.role import get_role
from app.crud.branch import get_branch
from app.exceptions.customError import CustomError
from app.utils.error_handler import handle_exception
from app.crud.branch import get_branch_company_id
from sqlalchemy import extract


def get_employee(db: Session, employee_id: int):
    from app.models.employee import Employee
    
    searched_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not searched_employee:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not fond")
    
    return searched_employee

def get_all_employees(db: Session,  skip: int = 0, limit: int = 100):
    from app.models.employee import Employee
    
    return db.query(Employee).offset(skip).limit(limit).all()

def get_employee_locks(db: Session, employee_id: int):
    from app.models.lock import Lock
    
    #Only 4 validation
    get_employee(db, employee_id)
    
    return db.query(Lock).filter(Lock.employee_id == employee_id).all()

def create_employee(db: Session, employee: EmployeeCreate):
    from app.models.employee import Employee
    
    try:
        #Only 4 validation
        get_branch(db, employee.branch_id)
        
        created_employee = Employee(name=employee.name, hourly_wage=employee.hourly_wage, monthly_hours=employee.monthly_hours, branch_id=employee.branch_id)
        
        db.add(created_employee)
        db.commit()
        db.refresh(created_employee)
        
        return created_employee
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error creating employee")

def update_employee(db:Session, employee_id: int, employee: EmployeeUpdate):
    
    try:
        searched_employee = get_employee(db, employee_id)
        
        update_data = employee.model_dump(exclude_unset=True)
        
        #Only 4 validation
        if "branch_id" in update_data:
            company_id = get_branch_company_id(db, update_data["branch_id"])
            if company_id != searched_employee.branch.company_id:
                raise CustomError(status_code=status.HTTP_409_CONFLICT, detail="Branch change rejected: cross-company assignment is not allowed.")
        
        for key, value in update_data.items():
            setattr(searched_employee, key, value)
            
        db.commit()
        db.refresh(searched_employee)
        return searched_employee
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating employee")

def delete_employee(db: Session, employee_id):
    try:
        searched_employee = get_employee(db, employee_id)
        db.delete(searched_employee)
        db.commit()
        
        return searched_employee
    except Exception as e:
        db.rollback()   
        handle_exception(e, "Internal error deleting employee")
    

def asign_employee_role(db: Session, employee_id: int, role_id: int):
    
    try:
        searched_employee = get_employee(db, employee_id)
        
        searched_role = get_role(db, role_id)
        
        if searched_role in searched_employee.roles:
            raise CustomError(status_code=status.HTTP_409_CONFLICT, detail="Employee already has that role")
        
        if searched_role.area.branch_id != searched_employee.branch_id:
            raise CustomError(status_code=status.HTTP_409_CONFLICT, detail="The role must belong to the same branch as the employee")
        
        searched_employee.roles.append(searched_role)
        db.commit()
        db.refresh(searched_employee)
        
        return searched_employee, searched_role
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error asigning role to employee")

def get_employee_roles(db: Session, employee_id: int):
    searched_employee = get_employee(db, employee_id)

    return searched_employee.roles

def calculate_emplyee_total_shift_hours(db: Session, month_number: int, year_number: int, employee_id: int):
    from app.models.shift import Shift

    shifts = db.query(Shift).filter(extract('year', Shift.date) == year_number, extract('month', Shift.date) == month_number, Shift.employee_id == employee_id).all()
    total_hours = 0
    for shift in shifts:
        duration = shift.end_date_time - shift.start_date_time
        total_hours += duration.total_seconds() / 3600
    return total_hours

