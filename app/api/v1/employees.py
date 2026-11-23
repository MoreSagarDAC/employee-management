from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeWithDepartment,
)
from app.services import employee as service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "", response_model=EmployeeWithDepartment, status_code=status.HTTP_201_CREATED
)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    return service.create_employee(db, data)


@router.get("", response_model=list[EmployeeWithDepartment])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department_id: int | None = None,
    db: Session = Depends(get_db),
):
    return service.list_employees(db, skip, limit, department_id)


@router.get("/{employee_id}", response_model=EmployeeWithDepartment)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return service.get_employee(db, employee_id)


@router.patch("/{employee_id}", response_model=EmployeeWithDepartment)
def update_employee(
    employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)
):
    return service.update_employee(db, employee_id, data)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    service.delete_employee(db, employee_id)