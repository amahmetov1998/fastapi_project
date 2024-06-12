from pydantic import BaseModel


class AssignLeaderSchema(BaseModel):
    position_id: int
    department_id: int
    user_id: int


class ReassignUserSchema(BaseModel):
    position_id: int
    user_id: int


class AssignUserSchema(BaseModel):
    position_id: int
    leader_position_id: int
    user_id: int
