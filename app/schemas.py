from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import constr


NonEmptyString = constr(strip_whitespace=True, min_length=1)


class StudentCreate(BaseModel):
    student_id: NonEmptyString
    name: NonEmptyString
    email: NonEmptyString
    major: NonEmptyString
    grade: int


class StudentResponse(BaseModel):
    id: int
    student_id: str
    name: str
    email: str
    major: str
    grade: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
