import pytest

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.database import get_db
from tests.database import TestingSessionLocal


@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    try:
        db.execute(
            text(
                "TRUNCATE TABLE students "
                "RESTART IDENTITY CASCADE"
            )
        )

        db.commit()

        yield

    finally:
        db.close()


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture 
def client():

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()