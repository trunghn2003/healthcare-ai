"""
Shared models for use across services in healthcare-ai system
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PatientBase(BaseModel):
    name: str
    date_of_birth: str
    gender: str
    contact: str
    medical_history: List[str] = []


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True


class PredictionFeatures(BaseModel):
    """Input features for disease prediction model"""
    features: List[float]


class PredictionResult(BaseModel):
    """Result from AI prediction model"""
    prediction: float
    probability: float
    disease_risk: str  # 'low', 'medium', 'high'
    status: str


class HealthAssessment(BaseModel):
    """Combined health assessment with patient data and prediction"""
    patient_id: str
    assessment_date: datetime
    prediction_result: PredictionResult
    recommendations: List[str] = []
    notes: Optional[str] = None
