from pydantic import BaseModel


class AddTaskSchema(BaseModel):
    title: str
    description: str
    author_id: int
    responsible_id: int
    observers_id: list[int]
    executors_id: list[int]
    deadline: str
    status: str
    time_estimation: str


class UpdateTaskNameSchema(BaseModel):
    old_title: str
    new_title: str


class DeleteTaskSchema(BaseModel):
    title: str
