"""
Shared models for use across services in healthcare-ai system
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date


class PatientBase(BaseModel):
    # Thông tin cá nhân
    full_name: str
    date_of_birth: date
    gender: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

    # Thông tin y tế
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree_function: float
    age: int


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: str
    diabetes_prediction: Optional[float] = None
    is_diabetic: Optional[bool] = None

    class Config:
        from_attributes = True
