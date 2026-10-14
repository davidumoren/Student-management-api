# =========================
# CREATE
# =========================

def test_create_student(client):

    student_data = {
        "name": "Test Student",
        "age": 25,
        "email": "teststudent@example.com",
        "phone": "08012345678",
        "is_active": True
    }

    response = client.post(
        "/students/",
        json=student_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Test Student"
    assert data["age"] == 25
    assert data["email"] == "teststudent@example.com"
    assert data["phone"] == "08012345678"
    assert data["is_active"] is True


# =========================
# READ ALL
# =========================

def test_read_students(client):

    response = client.get("/students/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =========================
# READ ONE
# =========================

def test_read_single_student(client):

    student_data = {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com",
        "phone": "08012345678",
        "is_active": True
    }

    create_response = client.post(
        "/students/",
        json=student_data
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.get(
        f"/students/{student_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["name"] == "John Doe"


# =========================
# READ NONEXISTENT
# =========================

def test_read_nonexistent_student(client):

    response = client.get("/students/99999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Student not found"


# =========================
# PUT
# =========================

def test_update_student_with_put(client):

    student_data = {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com",
        "phone": "08012345678",
        "is_active": True
    }

    create_response = client.post(
        "/students/",
        json=student_data
    )

    student_id = create_response.json()["id"]

    updated_data = {
        "name": "John Smith",
        "age": 30,
        "email": "johnsmith@example.com",
        "phone": "08099999999",
        "is_active": False
    }

    response = client.put(
        f"/students/{student_id}",
        json=updated_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "John Smith"
    assert data["age"] == 30
    assert data["email"] == "johnsmith@example.com"
    assert data["phone"] == "08099999999"
    assert data["is_active"] is False


# =========================
# PATCH
# =========================

def test_update_student_with_patch(client):

    student_data = {
        "name": "Jane Doe",
        "age": 28,
        "email": "jane@example.com",
        "phone": "08011111111",
        "is_active": True
    }

    create_response = client.post(
        "/students/",
        json=student_data
    )

    student_id = create_response.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={
            "age": 35
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["age"] == 35

    # These should remain unchanged
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["phone"] == "08011111111"
    assert data["is_active"] is True


# =========================
# PATCH NONEXISTENT
# =========================

def test_patch_nonexistent_student(client):

    response = client.patch(
        "/students/99999",
        json={
            "age": 30
        }
    )

    assert response.status_code == 404


# =========================
# DELETE
# =========================

def test_delete_student(client):

    student_data = {
        "name": "Delete Me",
        "age": 25,
        "email": "delete@example.com",
        "phone": "08022222222",
        "is_active": True
    }

    create_response = client.post(
        "/students/",
        json=student_data
    )

    student_id = create_response.json()["id"]

    response = client.delete(
        f"/students/{student_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Student deleted successfully"

    get_response = client.get(
        f"/students/{student_id}"
    )

    assert get_response.status_code == 404


# =========================
# DELETE NONEXISTENT
# =========================

def test_delete_nonexistent_student(client):

    response = client.delete(
        "/students/99999"
    )

    assert response.status_code == 404


# =========================
# DUPLICATE EMAIL
# =========================

def test_duplicate_email(client):

    student_data = {
        "name": "First Student",
        "age": 25,
        "email": "duplicate@example.com",
        "phone": "08033333333",
        "is_active": True
    }

    first_response = client.post(
        "/students/",
        json=student_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/students/",
        json=student_data
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == (
        "A student with this email already exists."
    )


# =========================
# INVALID EMAIL
# =========================

def test_invalid_email(client):

    student_data = {
        "name": "Invalid Email",
        "age": 25,
        "email": "not-an-email",
        "phone": "08044444444",
        "is_active": True
    }

    response = client.post(
        "/students/",
        json=student_data
    )

    assert response.status_code == 422


# =========================
# INVALID AGE
# =========================

def test_invalid_age(client):

    student_data = {
        "name": "Invalid Age",
        "age": 10,
        "email": "invalidage@example.com",
        "phone": "08055555555",
        "is_active": True
    }

    response = client.post(
        "/students/",
        json=student_data
    )

    assert response.status_code == 422


# =========================
# MISSING REQUIRED FIELD
# =========================

def test_missing_required_field(client):

    student_data = {
        "name": "Missing Phone",
        "age": 25,
        "email": "missingphone@example.com"
    }

    response = client.post(
        "/students/",
        json=student_data
    )

    assert response.status_code == 422