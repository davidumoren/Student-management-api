import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import models


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL environment variable is not set."
    )

engine = create_engine(TEST_DATABASE_URL)

if not engine.url.database.endswith("_test"):
    raise RuntimeError(
        "The test database name must end with '_test'."
    )

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

with engine.connect() as connection:
    print("Connected to the test database successfully.")