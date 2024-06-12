from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    name: str


class UpdateDepartmentSchema(BaseModel):
    id: int
    name: str
