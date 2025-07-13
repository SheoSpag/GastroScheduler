from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.schemas.shift import ShiftCreate, ShiftUpdate
from app.crud.role import get_role
from app.crud.employee import get_employee
from app.exceptions.customError import CustomError
from fastapi import status
from datetime import date, timedelta

from app.utils.error_handler import handle_exception

def get_shift(db: Session, shift_id:int):
    from app.models.shift import Shift
    searched_shift = db.query(Shift).filter(Shift.id == shift_id).first()
    
    if not searched_shift:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    return searched_shift

def get_all_shifts(db:Session, skip: int = 0, limit: int = 100):
    from app.models.shift import Shift
    
    return db.query(Shift).offset(skip).limit(limit).all()

def get_employee_shifts_by_month_number(db: Session, month_number: int, year_number: int, employee_id: int):
    from app.models.shift import Shift

    return db.query(Shift).filter(extract('year', Shift.date) == year_number, extract('month', Shift.date) == month_number, Shift.employee_id == employee_id).all()

def create_shift(db: Session, shift: ShiftCreate):
    from app.models.shift import Shift
    
    try:
        searched_employee = get_employee(db, shift.employee_id)
        
        searched_role = get_role(db, shift.role_id)
        
        if searched_role not in searched_employee.roles:
            raise CustomError(status_code=status.HTTP_409_CONFLICT, detail="The employee does not have the rol assigned")
        
        existing_shift = db.query(Shift).filter(Shift.employee_id == shift.employee_id, Shift.date == shift.date).first()
        
        if existing_shift:
            raise CustomError(status_code=status.HTTP_409_CONFLICT, detail="The employee already has a shift for that day")
        
        if shift.start_date_time > shift.end_date_time:
            raise CustomError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Shift end time must be after start time")
        
        created_shift = Shift(start_date_time= shift.start_date_time, end_date_time= shift.end_date_time, date= shift.date, employee_id= shift.employee_id, role_id= shift.role_id)
        
        db.add(created_shift)
        db.commit()
        db.refresh(created_shift)
        
        return created_shift
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error creating the shift")

def update_shift(db: Session, shift_id: int, shift: ShiftUpdate):
    try:
        searched_shift = get_shift(db, shift_id)

        updated_data = shift.model_dump(exclude_unset=True)
        
        employee = None
        role = None    
        
        if "employee_id" in updated_data:
            employee = get_employee(db, updated_data["employee_id"])
            if not employee:
                raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
            
        if "role_id" in updated_data:
            role = get_role(db, updated_data["role_id"])
            if not role:
                raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
            
        final_employee = employee or get_employee(db, searched_shift.employee_id)
        if role and role not in final_employee.roles:
            raise CustomError(status_code=409, detail="Employee does not have this role assigned")

        
        for key, value in updated_data.items():
            setattr(searched_shift, key, value)
            
        db.commit()
        db.refresh(searched_shift)
        
        return searched_shift
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the branch")

def delete_shift(db: Session, shift_id: int):
    try:
        searched_shift = get_shift(db, shift_id)
        
        db.delete(searched_shift)
        db.commit()
        
        return searched_shift
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error deleting the shift")