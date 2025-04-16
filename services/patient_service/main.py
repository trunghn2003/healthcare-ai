from fastapi import FastAPI, HTTPException
import httpx
from shared.models.patient import PatientCreate, PatientResponse
import uuid
from typing import List

app = FastAPI()

# In-memory database for demonstration
patients_db = {}

# AI service URL
AI_SERVICE_URL = "http://localhost:8001/predict"

@app.post("/patients/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate):
    try:
        # Generate patient ID
        patient_id = str(uuid.uuid4())

        # Get prediction from AI service
        async with httpx.AsyncClient() as client:
            response = await client.post(AI_SERVICE_URL, json=patient.dict())
            prediction_data = response.json()

        # Create patient record with prediction
        patient_data = {
            "id": patient_id,
            **patient.dict(),
            "diabetes_prediction": prediction_data["diabetes_prediction"],
            "is_diabetic": prediction_data["is_diabetic"]
        }

        # Save to database
        patients_db[patient_id] = patient_data

        return patient_data
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_id]

@app.get("/patients/", response_model=List[PatientResponse])
async def list_patients():
    return list(patients_db.values())

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
