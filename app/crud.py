from sqlalchemy.orm import Session

from app import models
from app import schemas


# CREATE STUDENT
def create_student(
    db: Session,
    student: schemas.StudentCreate
):
    db_student = models.Student(
        name=student.name,
        age=student.age,
        email=student.email,
        phone=student.phone,
        is_active=student.is_active
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student   


# READ ALL STUDENTS
def get_students(db: Session):
    return db.query(models.Student).all()


# READ ONE STUDENT
def get_student(
    db: Session,
    student_id: int
):
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()


# PUT - FULL UPDATE STUDENT
def update_student(
    db: Session,
    student_id: int,
    student_data: schemas.StudentPut
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        return None

    student.name = student_data.name
    student.age = student_data.age
    student.email = student_data.email
    student.phone = student_data.phone
    student.is_active = student_data.is_active

    db.commit()  
    db.refresh(student)

    return student


# PATCH - PARTIAL UPDATE STUDENT
def patch_student(
    db: Session,
    student_id: int,
    student_data: schemas.StudentUpdate
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        return None

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


# DELETE STUDENT
def delete_student(
    db: Session,
    student_id: int
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        return None

    db.delete(student)
    db.commit()

    return student