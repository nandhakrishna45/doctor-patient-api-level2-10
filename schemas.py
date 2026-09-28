from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


PHONE_PATTERN = r"^\d{10}$"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: str = Field(default="doctor", pattern=r"^(admin|doctor)$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DoctorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=100)
    email: EmailStr


class DoctorUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=100)
    email: EmailStr
    is_active: bool = True


class DoctorPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    specialization: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool


class PatientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0)
    phone: str = Field(pattern=PHONE_PATTERN)
    doctor_id: Optional[int] = None


class PatientUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0)
    phone: str = Field(pattern=PHONE_PATTERN)
    doctor_id: Optional[int] = None


class PatientPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(default=None, pattern=PHONE_PATTERN)
    doctor_id: Optional[int] = None


class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    phone: str
    doctor_id: Optional[int] = None


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int


class DoctorListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[DoctorResponse]


class PatientListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[PatientResponse]
