from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models
from app.database import get_db, engine, Base
from app.routers import students


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure SQLAlchemy has registered the Student model.
    # Create tables that are missing from the database.
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    students.router
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Student Management API"
    }


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "message": "Database connection successful!",
        "result": result.scalar()
    }


@app.get("/health/live")
def liveness_check():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ready"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )