from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Doctor, Patient


def get_doctor_or_404(db: Session, doctor_id: int) -> Doctor:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "doctor_not_found", "message": "Doctor does not exist"},
        )
    return doctor


def get_active_doctor_or_error(db: Session, doctor_id: int) -> Doctor:
    doctor = get_doctor_or_404(db, doctor_id)
    if not doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "inactive_doctor", "message": "Cannot assign a patient to an inactive doctor"},
        )
    return doctor


def get_patient_or_404(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "patient_not_found", "message": "Patient does not exist"},
        )
    return patient


def ensure_unique_doctor_email(
    db: Session, email: str, doctor_id: Optional[int] = None
) -> None:
    query = db.query(Doctor).filter(Doctor.email == email)
    if doctor_id is not None:
        query = query.filter(Doctor.id != doctor_id)

    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "duplicate_email", "message": "Doctor email already exists"},
        )


def validate_patient_doctor(db: Session, doctor_id: Optional[int]) -> None:
    if doctor_id is not None:
        get_active_doctor_or_error(db, doctor_id)
