from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes.idex_router import router
from app.middlewares.customError import CustomError

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"mensaje": "La API funciona correctamente"}

@app.exception_handler(CustomError)
async def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.details}
    )