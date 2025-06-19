from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Session

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "La API funciona correctamente"}