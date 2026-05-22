from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import re
from datetime import date


app = FastAPI(title="Employee Import API")

employees_db = {}

email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
date_pattern = r"^\d{4}-\d{2}-\d{2}$"


class Employee(BaseModel):
    employee_id: str | None = None
    name: str | None = None
    email: str | None = None
    department: str | None = None
    salary: int | float | str | None = None
    join_date: str | None = None
# from typing import Optional, Union

# class Employee(BaseModel):
#     employee_id: Optional[str] = None
#     name: Optional[str] = None
#     email: Optional[str] = None
#     department: Optional[str] = None
#     salary: Optional[Union[int, float, str]] = None
#     join_date: Optional[str] = None

@app.post("/api/employees", status_code=201)
def create_employee(employee: Employee):
    errors = []

    employee_id = "" if employee.employee_id is None else str(employee.employee_id).strip()
    name = "" if employee.name is None else str(employee.name).strip()
    email = "" if employee.email is None else str(employee.email).strip()
    department = "" if employee.department is None else str(employee.department).strip()
    join_date = "" if employee.join_date is None else str(employee.join_date).strip()
    salary = employee.salary

    # employee_id required
    if employee_id == "":
        errors.append("employee_id is required")

    # employee_id unique
    elif employee_id in employees_db:
        errors.append(f"employee_id {employee_id} already exists")

    # name required and length 1~50
    if name == "":
        errors.append("name is required")
    elif len(name) > 50:
        errors.append("name length must be between 1 and 50 characters")

    # email required and valid format
    if email == "":
        errors.append("email is required")
    elif not re.match(email_pattern, email):
        errors.append("email format is invalid")

    # department required
    if department == "":
        errors.append("department is required")

    # salary required and positive integer
    if salary is None or str(salary).strip() == "":
        errors.append("salary is required")
        salary_num = None
    else:
        try:
            salary_num = float(salary)
            if salary_num <= 0:
                errors.append("salary must be greater than 0")
            elif salary_num % 1 != 0:
                errors.append("salary must be an integer")
        except ValueError:
            salary_num = None
            errors.append("salary must be a number")

    # join_date required and valid YYYY-MM-DD
    if join_date == "":
        errors.append("join_date is required")
    elif not re.match(date_pattern, join_date):
        errors.append("join_date format must be YYYY-MM-DD")
    else:
        try:
            date.fromisoformat(join_date)
        except ValueError:
            errors.append("join_date must be a valid calendar date")

    # 有任何錯誤，就統一回 422
    if errors:
        raise HTTPException(
            status_code=422,
            detail=errors
        )

    employees_db[employee_id] = {
        "employee_id": employee_id,
        "name": name,
        "email": email,
        "department": department,
        "salary": int(salary_num),
        "join_date": join_date,
    }

    return {
        "id": employee_id,
        "status": "created"
    }


@app.get("/api/employees")
def list_employees():
    return list(employees_db.values())


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )