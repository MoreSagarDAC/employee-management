from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.department import Department
from app.repositories import department as repo
from app.schemas.department import DepartmentCreate, DepartmentUpdate


def get_department(db: Session, department_id: int) -> Department:
    department = repo.get(db, department_id)
    if not department:
        raise NotFoundError("Department not found")
    return department


def list_departments(db: Session, skip: int, limit: int) -> list[Department]:
    return repo.list_all(db, skip, limit)


def create_department(db: Session, data: DepartmentCreate) -> Department:
    if repo.get_by_name(db, data.name):
        raise ConflictError("Department name already exists")
    return repo.create(db, data)


def update_department(
    db: Session, department_id: int, data: DepartmentUpdate
) -> Department:
    department = get_department(db, department_id)

    if data.name and data.name != department.name:
        if repo.get_by_name(db, data.name):
            raise ConflictError("Department name already exists")

    return repo.update(db, department, data)


def delete_department(db: Session, department_id: int) -> None:
    department = get_department(db, department_id)
    try:
        repo.delete(db, department)
    except IntegrityError:
        db.rollback()
        raise ConflictError("Cannot delete a department that has employees")