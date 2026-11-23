from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.department import DepartmentCreate, DepartmentOut, DepartmentUpdate
from app.services import department as service

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    return service.create_department(db, data)


@router.get("", response_model=list[DepartmentOut])
def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_departments(db, skip, limit)


@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(department_id: int, db: Session = Depends(get_db)):
    return service.get_department(db, department_id)


@router.patch("/{department_id}", response_model=DepartmentOut)
def update_department(
    department_id: int, data: DepartmentUpdate, db: Session = Depends(get_db)
):
    return service.update_department(db, department_id, data)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    service.delete_department(db, department_id)