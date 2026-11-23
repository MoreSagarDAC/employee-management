from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import departments, employees
from app.core.exceptions import AppError

app = FastAPI(title="Employee Management API", version="1.0.0")


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(departments.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}