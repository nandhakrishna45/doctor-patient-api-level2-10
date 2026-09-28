# Doctor Patient Management API — Level 2–10

A modular FastAPI backend implementing doctor-patient relationships, complete CRUD, validation, filtering, pagination, SQLAlchemy persistence, JWT authentication and production-oriented improvements.

## Features

- One-to-many Doctor → Patient relationship through `Patient.doctor_id`
- Prevent assignment to missing or inactive doctors
- Doctor and Patient CRUD
- PUT and PATCH support
- Soft delete for doctors
- Exact 10-digit numeric phone validation
- Unique doctor email validation
- Filtering
- Database-side pagination
- SQLAlchemy + SQLite
- JWT authentication and role-based authorization
- Logging
- Configurable CORS
- Environment variables
- API versioning with `/api/v1`
- Dockerfile
- Pytest-ready dependencies

## Structure

```text
doctor-patient-api2/
├── main.py
├── models.py
├── schemas.py
├── services.py
├── auth.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── doctors.py
│   └── patients.py
├── requirements.txt
├── .env.example
├── .gitignore
└── Dockerfile
```

## Setup

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a strong `SECRET_KEY`.

## Run

```bash
python -m uvicorn main:app --reload
```

Swagger:
`http://127.0.0.1:8000/docs`

## Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

Protected APIs require:

```text
Authorization: Bearer <token>
```

## Doctor APIs

```text
POST   /api/v1/doctors
GET    /api/v1/doctors
GET    /api/v1/doctors/{doctor_id}
PUT    /api/v1/doctors/{doctor_id}
PATCH  /api/v1/doctors/{doctor_id}
DELETE /api/v1/doctors/{doctor_id}
GET    /api/v1/doctors/{doctor_id}/patients
```

Doctor listing supports:

```text
GET /api/v1/doctors?specialization=cardiology
GET /api/v1/doctors?is_active=true
GET /api/v1/doctors?page=1&limit=10
```

## Patient APIs

```text
POST   /api/v1/patients
GET    /api/v1/patients
GET    /api/v1/patients/{patient_id}
PUT    /api/v1/patients/{patient_id}
PATCH  /api/v1/patients/{patient_id}
DELETE /api/v1/patients/{patient_id}
```

Patient filtering and pagination:

```text
GET /api/v1/patients?age_gt=30
GET /api/v1/patients?page=1&limit=10
```

Create a patient with an existing active doctor:

```json
{
  "name": "John Doe",
  "age": 35,
  "phone": "9876543210",
  "doctor_id": 1
}
```

## Validation

- Doctor email must be unique.
- Patient phone must contain exactly 10 numeric digits.
- Patient age must be greater than zero.
- A patient cannot be assigned to a non-existing doctor.
- A patient cannot be assigned to an inactive doctor.
- Missing doctors return HTTP 404.
- Inactive doctor assignment returns HTTP 400.
- Unauthorized requests return HTTP 401/403 as appropriate.

## Pagination Response

```json
{
  "total": 25,
  "page": 1,
  "limit": 10,
  "data": []
}
```

## Database

SQLite is used by default. SQLAlchemy manages sessions through a FastAPI dependency.

For a fresh schema during development, delete the local `app.db` and restart the application.

## Docker

```bash
docker build -t doctor-patient-api .
docker run -p 8000:8000 --env-file .env doctor-patient-api
```

## Testing

Install dependencies and run:

```bash
pytest
```

## API Versioning

All business APIs are versioned under:

```text
/api/v1
```

## Notes

The SQLite database file is intentionally excluded from Git using `.gitignore`. Do not commit `.env` or local database files.
