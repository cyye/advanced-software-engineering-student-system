from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.database import get_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Student Management System", lifespan=lifespan)


@app.get("/students", response_model=List[schemas.StudentResponse])
def list_students(db: Session = Depends(get_db)) -> list[schemas.StudentResponse]:
    return services.get_all_students(db)


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)) -> schemas.StudentResponse:
    student = services.get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
