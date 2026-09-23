from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate


class DuplicateStudentError(ValueError):
    pass


def get_all_students(db: Session) -> list[Student]:
    return db.query(Student).order_by(Student.id).all()


def get_student_by_id(db: Session, student_id: str) -> Student | None:
    return db.query(Student).filter(Student.student_id == student_id).first()


def create_student(db: Session, student_data: StudentCreate) -> Student:
    existing_student_id = db.query(Student).filter(Student.student_id == student_data.student_id).first()
    if existing_student_id is not None:
        raise DuplicateStudentError("Student ID already exists")

    existing_email = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_email is not None:
        raise DuplicateStudentError("Email already exists")

    student = Student(**student_data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
