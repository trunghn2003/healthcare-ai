"""
Shared models for use across services in healthcare-ai system
"""
from pydantic import BaseModel
from typing import Optional


class PatientBase(BaseModel):
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
