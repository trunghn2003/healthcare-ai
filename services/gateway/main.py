from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from shared.models.patient import PatientCreate, PatientResponse
from typing import List

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
PATIENT_SERVICE_URL = "http://localhost:8002"
AI_SERVICE_URL = "http://localhost:8001"

@app.post("/api/patients/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{PATIENT_SERVICE_URL}/patients/", json=patient.dict())
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Patient service unavailable")

@app.get("/api/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PATIENT_SERVICE_URL}/patients/{patient_id}")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Patient service unavailable")

@app.get("/api/patients/", response_model=List[PatientResponse])
async def list_patients():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PATIENT_SERVICE_URL}/patients/")
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Patient service unavailable")

@app.get("/api/health")
async def health_check():
    async with httpx.AsyncClient() as client:
        health_status = {"gateway": "healthy"}
        try:
            await client.get(f"{PATIENT_SERVICE_URL}/health")
            health_status["patient_service"] = "healthy"
        except httpx.RequestError:
            health_status["patient_service"] = "unhealthy"

        try:
            await client.get(f"{AI_SERVICE_URL}/health")
            health_status["ai_service"] = "healthy"
        except httpx.RequestError:
            health_status["ai_service"] = "unhealthy"

        return health_status

@app.post("/api/predict")
async def predict_diabetes(patient_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            # Chuyển tiếp yêu cầu đến AI Service
            ai_response = await client.post(f"{AI_SERVICE_URL}/predict", json=patient_data)
            ai_response.raise_for_status()
            prediction_result = ai_response.json()

            # Lưu kết quả dự đoán cùng với dữ liệu bệnh nhân vào Patient Service
            patient_with_prediction = {**patient_data, **prediction_result}
            await client.post(f"{PATIENT_SERVICE_URL}/patients/", json=patient_with_prediction)

            return prediction_result
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code,
                               detail=f"AI Service error: {e.response.text}")
        except httpx.RequestError:
            raise HTTPException(status_code=503,
                               detail="AI Service unavailable")
