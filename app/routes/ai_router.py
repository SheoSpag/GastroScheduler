from fastapi import APIRouter
from pydantic import BaseModel
from app.models.shift import Shift
from app.utils.prompt_builder import build_weekly_shifts
from app.db.db import get_db
from sqlalchemy.orm import Session
from typing import List
from app.schemas.shift import ShiftCreate
from fastapi import status
from datetime import datetime, date

from fastapi import Depends


router = APIRouter()

class MessageInput(BaseModel):
    message: str

@router.post("/generate-weekly-shifts/branch/{branch_id}", status_code=status.HTTP_201_CREATED)
def generate_weekly_shifts(branch_id: int, db: Session = Depends(get_db)):
    try:
        ai_shifts = build_weekly_shifts(branch_id, db) 
        data = create_shifts_bulk(ai_shifts, db)
        return data
    except Exception as e:
        import traceback
        traceback.print_exc()  
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=422, content={"error": str(e)})



def create_shifts_bulk(shifts: List[dict], db: Session = Depends(get_db)):
    try:
        all_shifts = []
        for shift_data in shifts:
            shift = ShiftCreate(**shift_data)
            
            start_dt = shift.start_date_time if isinstance(shift.start_date_time, datetime) else datetime.fromisoformat(shift.start_date_time)
            end_dt = shift.end_date_time if isinstance(shift.end_date_time, datetime) else datetime.fromisoformat(shift.end_date_time)
            shift_date = shift.date if isinstance(shift.date, date) else date.fromisoformat(shift.date)
            

            all_shifts.append(
                Shift(
                    start_date_time = start_dt,
                    end_date_time = end_dt,
                    date = shift_date,
                    role_id = shift.role_id,
                    employee_id = shift.employee_id
                )
            )
        db.add_all(all_shifts)
        db.commit()
        
        return {"message": f"Created {len(shifts)} shifts successfully"}
    except Exception as e:
        db.rollback()
        raise e
    

