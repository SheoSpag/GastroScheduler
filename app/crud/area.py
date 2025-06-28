from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.area import AreaCreate, AreaUpdate

 
def get_area(db: Session, area_id: int):
    from app.models.area import Area
    
    return db.query(Area).filter(Area.id == area_id).first()

def get_areas(db: Session, skip: int = 0, limit: int = 0):
    from app.models.area import Area
    
    return db.query(Area).offset(skip).limit(limit).all()

def create_area(db: Session, area: AreaCreate):
    from app.models.area import Area
    
    created_area = Area(opening_time= area.opening_time, closing_time= area.closing_time, minimum_staff= area.maximum_staff, maximum_staff=area.minimum_staff, name=area.name)
    
    db.add(created_area)
    db.commit()
    db.refresh(created_area)
    return created_area

def update_area(db: Session, area_id: int, area: AreaUpdate):
    searched_area = get_area(db, area_id)
    
    if not searched_area:
        return None
    
    update_data = area.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(searched_area, key, value)
        
    db.commit()
    db.refresh(searched_area)
    return searched_area

def delete_area(db: Session, area_id: int):
    searched_area = get_area(db, area_id)
    
    if not searched_area:
        return None
    
    db.delete(searched_area)
    db.commit()
    
    return searched_area
    
    
        
    
    
        