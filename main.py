from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import Base

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "La API funciona correctamente"}