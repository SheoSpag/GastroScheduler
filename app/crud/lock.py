from sqlalchemy.orm import Session
from app.schemas.lock import LockCreate, LockUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.exceptions.customError import CustomError
from app.utils.error_handler import handle_exception

from app.crud.employee import get_employee

def get_lock(db: Session, lock_id: int):
    from app.models.lock import Lock
    searched_lock = db.query(Lock).filter(Lock.id == lock_id).first()
    if not searched_lock:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Lock not found")
    return searched_lock

def get_all_locks(db: Session, skip: int = 0, limit: int = 100):
    from app.models.lock import Lock
    
    return db.query(Lock).offset(skip).limit(limit).all()


def create_lock(db: Session, lock: LockCreate):
    from app.models.lock import Lock
  
    try:
        #Only 4 validation 
        get_employee(db, lock.employee_id)
        
        #Only 4 validation
        already_a_lock = db.query(Lock).filter(Lock.employee_id == lock.employee_id, Lock.locked_date == lock.locked_date).first()
        
        if already_a_lock:
            raise CustomError(status_code=status.HTTP_409_CONFLICT, detail="There is already a block for that employee on that date")
        
        created_lock = Lock(locked_date=lock.locked_date,  note=lock.note, lock_reason=lock.lock_reason, employee_id=lock.employee_id)
        
        db.add(created_lock)
        db.commit()
        db.refresh(created_lock)
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error creating the lock")
        

    return created_lock

def delete_lock(db: Session, lock_id: int):
    try:
        searched_lock = get_lock(db, lock_id)
        
        db.delete(searched_lock)
        db.commit()
        
        return searched_lock
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error deleting the lock")
    

def update_lock(db: Session, lock_id: int, lock: LockUpdate):
    try:
        searched_lock = get_lock(db, lock_id)
        
        update_data = lock.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(searched_lock, key, value)
            
        db.commit()
        db.refresh(searched_lock)
        return searched_lock
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the lock")
    
    