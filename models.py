import os

from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=False)
    role = Column(String(20), nullable=False, default="doctor")
    is_active = Column(Boolean, nullable=False, default=True)

    doctor = relationship("Doctor", back_populates="user", uselist=False)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)

    user = relationship("User", back_populates="doctor")
    patients = relationship("Patient", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(10), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True, index=True)

    doctor = relationship("Doctor", back_populates="patients")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
