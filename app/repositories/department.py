from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


def get(db: Session, department_id: int) -> Department | None:
    return db.get(Department, department_id)


def get_by_name(db: Session, name: str) -> Department | None:
    return db.scalar(select(Department).where(Department.name == name))


def list_all(db: Session, skip: int = 0, limit: int = 10) -> list[Department]:
    stmt = select(Department).order_by(Department.id).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create(db: Session, data: DepartmentCreate) -> Department:
    department = Department(**data.model_dump())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


def update(db: Session, department: Department, data: DepartmentUpdate) -> Department:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(department, field, value)
    db.commit()
    db.refresh(department)
    return department


def delete(db: Session, department: Department) -> None:
    db.delete(department)
    db.commit()