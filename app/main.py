from fastapi import FastAPI

from app.api.v1 import departments, employees

app = FastAPI(title="Employee Management API", version="1.0.0")

app.include_router(departments.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}