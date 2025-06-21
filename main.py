from fastapi import FastAPI, Depends, HTTPException
from app.db.db import Base
from app.routes.idex_router import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"mensaje": "La API funciona correctamente"}