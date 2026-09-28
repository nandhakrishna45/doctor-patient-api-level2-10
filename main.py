import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Base, engine
from routes.doctors import router as doctors_router
from routes.patients import router as patients_router
from routes.auth import router as auth_router

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doctor Patient Management API",
    description="Production-ready FastAPI backend with JWT authentication, role-based authorization, doctor-patient relationships, CRUD, filtering and pagination.",
    version="2.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=f"{API_PREFIX}/auth", tags=["Authentication"])
app.include_router(doctors_router, prefix=f"{API_PREFIX}/doctors", tags=["Doctors"])
app.include_router(patients_router, prefix=f"{API_PREFIX}/patients", tags=["Patients"])


@app.get("/")
def root():
    return {
        "message": "Doctor Patient Management API",
        "version": "2.0.0",
        "documentation": "/docs",
        "api_prefix": API_PREFIX,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
