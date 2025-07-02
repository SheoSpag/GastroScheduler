from sqlalchemy.orm import Session
from app.schemas.role import RoleCreate, RoleUpdate
from app.utils.error_handler import handle_exception
from app.exceptions.customError import CustomError
from app.crud.area import get_area
from fastapi import status

def get_role(db: Session, role_id: int):
    from app.models.role import Role
    searched_role = db.query(Role).filter(Role.id == role_id).first()
    
    if not searched_role:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return searched_role

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    from app.models.role import Role
    
    return db.query(Role).offset(skip).limit(limit).all()

def get_role_employees(db: Session, role_id: int):
    searched_role = get_role(db, role_id)
    
    return searched_role.employees
    

def create_role(db: Session, role: RoleCreate):
    from app.models.role import Role
    
    try:
        #Just 4 validation
        get_area(db, role.area_id)
        
        created_role = Role(name=role.name, area_id=role.area_id)
        
        db.add(created_role)
        db.commit()
        db.refresh(created_role)
        return created_role
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error creating the role")

def update_role(db: Session, role_id: int, role: RoleUpdate):
    try:
        #Just 4 validation
        searched_role = get_role(db, role_id)
        
        update_date = role.model_dump(exclude_unset=True)
        
        for key, value in update_date.items():
            setattr(searched_role, key, value)
            
        db.commit()
        db.refresh(searched_role)
        return searched_role
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the role")

def delete_role(db: Session, role_id: int):
    try:
        #Just 4 validation
        searched_role = get_role(db, role_id)
        
        db.delete(searched_role)
        db.commit()
        
        return searched_role
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error deleting the role")

        