from sqlalchemy.orm import Session
from app.schemas.area import AreaCreate, AreaUpdate
from app.crud.branch import get_branch

from app.exceptions.customError import CustomError
from fastapi import status
from app.utils.error_handler import handle_exception
 
def get_area(db: Session, area_id: int):
    from app.models.area import Area
    searched_area = db.query(Area).filter(Area.id == area_id).first()

    if not searched_area:
        raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return searched_area

def get_areas(db: Session, skip: int = 0, limit: int = 0):
    from app.models.area import Area
    
    return db.query(Area).offset(skip).limit(limit).all()

def create_area(db: Session, area: AreaCreate):
    from app.models.area import Area
    try:        
        #just 4 valitadion
        searched_branch = get_branch(db, area.branch_id)
        
        if not searched_branch:
            raise CustomError(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
        
        if area.minimum_staff > area.maximum_staff:
            raise CustomError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Minimum staff cannot be greater than maximum staff")

        created_area = Area(opening_time= area.opening_time, closing_time= area.closing_time, minimum_staff= area.minimum_staff, maximum_staff=area.maximum_staff, name=area.name, branch_id=area.branch_id)
        
        db.add(created_area)
        db.commit()
        db.refresh(created_area)
        return created_area
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error creating area")

def update_area(db: Session, area_id: int, area: AreaUpdate):
    try:
        searched_area = get_area(db, area_id)
        
        update_data = area.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(searched_area, key, value)
            
        if "minimum_staff" in update_data and  update_data["minimum_staff"] == 0:
            raise CustomError(status_code=status.HTTP_400_BAD_REQUEST, detail="Minimum staff must be greater than zero")
            
        db.commit()
        db.refresh(searched_area)
        return searched_area
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error updating the area")

def delete_area(db: Session, area_id: int):
    try:
        #Just 4 validartion
        searched_area = get_area(db, area_id)
        
        db.delete(searched_area)
        db.commit()
        
        return searched_area
    except Exception as e:
        db.rollback()
        handle_exception(e, "Internal error deleting the area")
    
    
        
    
    
        