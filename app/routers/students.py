from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import crud
from app import schemas
from app.database import get_db


router = APIRouter(
    prefix="/students",
    tags=["students"]
)


# CREATE STUDENT
@router.post(
    "/",
    response_model=schemas.StudentResponse,
    status_code=201
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_student(
            db,
            student
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists."
        )


# READ ALL STUDENTS
@router.get(
    "/",
    response_model=list[schemas.StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):
    return crud.get_students(db)


# READ ONE STUDENT
@router.get(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(
        db,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# PUT - FULL UPDATE
@router.put(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def update_student(
    student_id: int,
    student: schemas.StudentPut,
    db: Session = Depends(get_db)
):
    updated_student = crud.update_student(
        db,
        student_id,
        student
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


# PATCH - PARTIAL UPDATE
@router.patch(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def patch_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    updated_student = crud.patch_student(
        db,
        student_id,
        student
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


# DELETE STUDENT
@router.delete(
    "/{student_id}"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    deleted_student = crud.delete_student(
        db,
        student_id
    )

    if deleted_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }