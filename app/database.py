from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models import Student

    Base.metadata.create_all(bind=engine)

    sample_students = [
        Student(
            student_id="20260001",
            name="Alice Zhang",
            email="alice@example.com",
            major="Computer Science",
            grade=2026,
        ),
        Student(
            student_id="20260002",
            name="Bob Li",
            email="bob@example.com",
            major="Software Engineering",
            grade=2026,
        ),
        Student(
            student_id="20250001",
            name="Carol Wang",
            email="carol@example.com",
            major="Computer Science",
            grade=2025,
        ),
    ]

    with SessionLocal() as db:
        has_students = db.query(Student).first() is not None
        if has_students:
            return

        db.add_all(sample_students)
        db.commit()
