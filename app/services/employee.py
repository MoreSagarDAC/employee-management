from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.employee import Employee
from app.repositories import department as department_repo
from app.repositories import employee as repo
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int) -> Employee:
    employee = repo.get(db, employee_id)
    if not employee:
        raise NotFoundError("Employee not found")
    return employee


def list_employees(
    db: Session, skip: int, limit: int, department_id: int | None = None
) -> list[Employee]:
    return repo.list_all(db, skip, limit, department_id)


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    if not department_repo.get(db, data.department_id):
        raise NotFoundError("Department not found")
    if repo.get_by_email(db, data.email):
        raise ConflictError("Email already registered")
    return repo.create(db, data)


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> Employee:
    employee = get_employee(db, employee_id)

    if data.department_id and not department_repo.get(db, data.department_id):
        raise NotFoundError("Department not found")
    if data.email and data.email != employee.email:
        if repo.get_by_email(db, data.email):
            raise ConflictError("Email already registered")

    repo.update(db, employee, data)
    return get_employee(db, employee_id)  # reload with department


def delete_employee(db: Session, employee_id: int) -> None:
    employee = get_employee(db, employee_id)
    repo.delete(db, employee)