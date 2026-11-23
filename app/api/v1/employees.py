from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories import department as department_repo
from app.repositories import employee as repo
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeWithDepartment,
)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "", response_model=EmployeeWithDepartment, status_code=status.HTTP_201_CREATED
)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    if not department_repo.get(db, data.department_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Department not found")
    if repo.get_by_email(db, data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    return repo.create(db, data)


@router.get("", response_model=list[EmployeeWithDepartment])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department_id: int | None = None,
    db: Session = Depends(get_db),
):
    return repo.list_all(db, skip, limit, department_id)


@router.get("/{employee_id}", response_model=EmployeeWithDepartment)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = repo.get(db, employee_id)
    if not employee:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")
    return employee


@router.patch("/{employee_id}", response_model=EmployeeWithDepartment)
def update_employee(
    employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)
):
    employee = repo.get(db, employee_id)
    if not employee:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")

    if data.department_id and not department_repo.get(db, data.department_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Department not found")
    if data.email and data.email != employee.email and repo.get_by_email(db, data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    repo.update(db, employee, data)
    return repo.get(db, employee_id)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = repo.get(db, employee_id)
    if not employee:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")
    repo.delete(db, employee)