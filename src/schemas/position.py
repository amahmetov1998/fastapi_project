from pydantic import BaseModel


class AddPositionSchema(BaseModel):
    position_name: str
    department_name: str


class UpdatePositionSchema(BaseModel):
    old_position_name: str
    new_position_name: str


class DeletePositionSchema(BaseModel):
    position_name: str
