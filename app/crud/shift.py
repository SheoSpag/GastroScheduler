from sqlalchemy.orm import Session
from app.schemas.shift import ShiftCreate, ShiftUpdate
from app.crud.role import get_role
from app.crud.employee import get_employee

def get_shift(db: Session, shift_id:int):
    from app.models.shift import Shift
    
    return db.query(Shift).filter(Shift.id == shift_id).first()

def get_all_shifts(db:Session, skip: int = 0, limit: int = 100):
    from app.models.shift import Shift
    
    return db.query(Shift).offset(skip).limit(limit).all()

def create_shift(db: Session, shift: ShiftCreate):
    from app.models.shift import Shift
    
    searched_employee = get_employee(db, shift.employee_id)
    
    if not searched_employee:
        return None
    
    searched_role = get_role(db, shift.role_id)
    
    if not searched_employee:
        return None
    
    if searched_role not in searched_employee.roles:
        return None
    
    existing_shift = db.query(Shift).filter(Shift.employee_id == shift.employee_id, Shift.date == shift.date).first()
    
    if existing_shift:
        return None
    
    created_shift = Shift(start_date_time= shift.start_date_time, end_date_time= shift.end_date_time, date= shift.date, employee_id= shift.employee_id, role_id= shift.role_id)
    
    db.add(created_shift)
    db.commit()
    db.refresh(created_shift)
    
    return created_shift

def update_shift(db: Session, shift_id: int, shift: ShiftUpdate):
    
    searched_shift = get_shift(db, shift_id)
    
    if not searched_shift:
        return None
    
    updated_data = shift.model_dump(exclude_unset=True)
    
    employee = None
    role = None    
    
    if "employee_id" in updated_data:
        employee = get_employee(db, updated_data["employee_id"])
        if not employee:
            return None
        
    if "role_id" in updated_data:
        role = get_role(db, updated_data["role_id"])
        if not role:
            return None
        
    if employee and role:
        if role not in employee.roles:
            return None 
        
        
    
    for key, value in updated_data.items():
        setattr(searched_shift, key, value)
        
    db.commit()
    db.refresh(searched_shift)
    
    return searched_shift

def delete_shift(db: Session, shift_id: int):
    searched_shift = get_shift(db, shift_id)
    
    if not searched_shift:
        return None
    
    db.delete(searched_shift)
    db.commit()
    
    return searched_shift