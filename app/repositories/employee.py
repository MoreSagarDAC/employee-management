from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get(db: Session, employee_id: int) -> Employee | None:
    stmt = (
        select(Employee)
        .options(selectinload(Employee.department))  # avoids N+1 queries
        .where(Employee.id == employee_id)
    )
    return db.scalar(stmt)


def get_by_email(db: Session, email: str) -> Employee | None:
    return db.scalar(select(Employee).where(Employee.email == email))


def list_all(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    department_id: int | None = None,
) -> list[Employee]:
    stmt = select(Employee).options(selectinload(Employee.department))
    if department_id is not None:
        stmt = stmt.where(Employee.department_id == department_id)
    stmt = stmt.order_by(Employee.id).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create(db: Session, data: EmployeeCreate) -> Employee:
    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    return get(db, employee.id)  # reload with department


def update(db: Session, employee: Employee, data: EmployeeUpdate) -> Employee:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()