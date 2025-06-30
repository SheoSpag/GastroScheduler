from sqlalchemy.orm import Session
from app.schemas.role import RoleCreate, RoleUpdate

def get_role(db: Session, role_id: int):
    from app.models.role import Role
    
    return db.query(Role).filter(Role.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    from app.models.role import Role
    
    return db.query(Role).offset(skip).limit(limit).all()

def get_role_employees(db: Session, role_id: int):
    searched_role = get_role(db, role_id)
    
    if not searched_role:
        return None
    
    return searched_role.employees
    

def create_role(db: Session, role: RoleCreate):
    from app.models.role import Role
    
    created_role = Role(name=role.name, area_id=role.area_id)
    
    db.add(created_role)
    db.commit()
    db.refresh(created_role)
    return created_role

def update_role(db: Session, role_id: int, role: RoleUpdate):
    searched_role = get_role(db, role_id)
    
    if not searched_role:
        return None
    
    update_date = role.model_dump(exclude_unset=True)
    
    for key, value in update_date.items():
        setattr(searched_role, key, value)
        
    db.commit()
    db.refresh(searched_role)
    return searched_role

def deleted_role(db: Session, role_id: int):
    searched_role = get_role(db, role_id)
    
    if not searched_role:
        return None
    
    db.delete(searched_role)
    db.commit()
    
    return searched_role

        