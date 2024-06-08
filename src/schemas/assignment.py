from pydantic import BaseModel


class AssignLeaderSchema(BaseModel):
    position_name: str
    department_name: str
    first_name: str
    last_name: str


class ReassignSchema(BaseModel):
    position_name: str
    first_name: str
    last_name: str


class AssignUserSchema(BaseModel):
    position_name: str
    leader_position: str
    first_name: str
    last_name: str
