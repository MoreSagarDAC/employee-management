from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.department import DepartmentOut


class EmployeeBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    salary: Decimal = Field(gt=0)
    hire_date: date
    department_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    salary: Decimal | None = Field(default=None, gt=0)
    hire_date: date | None = None
    department_id: int | None = None
    is_active: bool | None = None


class EmployeeOut(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class EmployeeWithDepartment(EmployeeOut):
    department: DepartmentOut