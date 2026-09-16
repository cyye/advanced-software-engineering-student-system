from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentResponse(BaseModel):
    id: int
    student_id: str
    name: str
    email: str
    major: str
    grade: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
