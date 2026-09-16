from sqlalchemy.orm import Session

from app.models import Student


def get_all_students(db: Session) -> list[Student]:
    return db.query(Student).order_by(Student.id).all()


def get_student_by_id(db: Session, student_id: str) -> Student | None:
    return db.query(Student).filter(Student.student_id == student_id).first()
