import datetime

from pydantic import BaseModel, Field

class TaskRecord(BaseModel):
    id: int
    name: str
    description: str = ""
    created_at: datetime.datetime

class ListTasksResponse(BaseModel):
    tasks: list[TaskRecord]

class CreateTaskRequest(BaseModel):
    name: str = Field(max_length=100)
    description: str = ""