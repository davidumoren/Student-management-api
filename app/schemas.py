from pydantic import BaseModel, EmailStr, Field


# =========================
# CREATE STUDENT
# =========================

class StudentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=16,
        le=120
    )

    email: EmailStr

    phone: str = Field(
        min_length=7,
        max_length=20
    )

    is_active: bool = True


# =========================
# RESPONSE
# =========================

class StudentResponse(BaseModel):

    id: int

    name: str

    age: int = Field(
        ge=16,
        le=120
    )

    email: EmailStr

    phone: str = Field(
        min_length=7,
        max_length=20
    )

    is_active: bool


# =========================
# PATCH - PARTIAL UPDATE
# =========================

class StudentUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    age: int | None = Field(
        default=None,
        ge=16,
        le=120
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20
    )

    is_active: bool | None = None


# =========================
# PUT - FULL UPDATE
# =========================

class StudentPut(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=16,
        le=120
    )

    email: EmailStr

    phone: str = Field(
        min_length=7,
        max_length=20
    )

    is_active: bool = True