from fastapi import APIRouter
from pydantic import BaseModel
from ai_client import generate_shifts

router = APIRouter()

class MessageInput(BaseModel):
    message: str

@router.post("/test")
def test_ai(payload: MessageInput):
    prompt = f"Respondé de forma breve y amable a esto: {payload.message}"
    response = generate_shifts(prompt)
    return {"respuesta_ia": response}
