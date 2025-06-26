from sqlalchemy.orm import Session
from app.schemas.lock import LockCreate, LockUpdate

def get_lock(db: Session, lock_id: int):
    from app.models.lock import Lock
    return db.query(Lock).filter(Lock.id == lock_id).first()

def get_all_locks(db: Session, skip: int = 0, limit: int = 100):
    from app.models.lock import Lock
    
    return db.query(Lock).offset(skip).limit(limit).all()


def create_lock(db: Session, lock: LockCreate):
    from app.models.lock import Lock

    created_lock = Lock(locked_date=lock.locked_date,  note=lock.note, reason=lock.lock_reason, employee_id=lock.employee_id)
    
    db.add(created_lock)
    db.commit()
    db.refresh(create_lock)
    
    return created_lock

def delete_lock(db: Session, lock_id: int):
    searched_lock = get_lock(db, lock_id)
    if not searched_lock: 
        return None
    
    db.delete(searched_lock)
    db.commit()
    
    return searched_lock

def update_lock(db: Session, lock_id: int, lock: LockUpdate):
    searched_lock = get_lock(db, lock_id)
    if not searched_lock:
        return None
    
    update_data = lock.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(searched_lock, key, value)
        
    db.commit()
    db.refresh(searched_lock)
    return searched_lock
    
    