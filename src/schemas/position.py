from pydantic import BaseModel


class AddPositionSchema(BaseModel):
    position_name: str
    department_name: str


class UpdatePositionSchema(BaseModel):
    id: int
    new_position_name: str
