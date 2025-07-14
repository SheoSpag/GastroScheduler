from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_client import generate_shifts
from app.utils.prompt_builder import build_weekly_shifts
from app.db.db import get_db
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import Depends


router = APIRouter()

class MessageInput(BaseModel):
    message: str

@router.post("/test")
def test_ai(payload: MessageInput):
    prompt = f"Respondé de forma breve y amable a esto: {payload.message}"
    response = generate_shifts(prompt)
    return {"respuesta_ia": response}

@router.post("/generate-weekly-shifts/branch/{branch_id}", status_code=status.HTTP_200_OK)
def generate_weekly_shifts(branch_id: int, db: Session = Depends(get_db)):
    prompt = build_weekly_shifts(branch_id, db)

    response = generate_shifts(prompt)
    return {"respuesta_ia": response}
    
    
