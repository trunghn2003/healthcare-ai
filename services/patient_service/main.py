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
async def create_patient(patient: dict):
    try:
        # Generate patient ID
        patient_id = str(uuid.uuid4())

        # Kiểm tra xem dữ liệu đã có kết quả dự đoán từ Gateway chưa
        if "diabetes_prediction" in patient and "is_diabetic" in patient:
            # Sử dụng kết quả dự đoán đã có
            patient_data = {
                "id": patient_id,
                **patient
            }
        else:
            # Nếu chưa có kết quả dự đoán, gọi AI Service
            async with httpx.AsyncClient() as client:
                response = await client.post(AI_SERVICE_URL, json=patient)
                prediction_data = response.json()

            patient_data = {
                "id": patient_id,
                **patient,
                "diabetes_prediction": prediction_data["diabetes_prediction"],
                "is_diabetic": prediction_data["is_diabetic"]
            }

        # In thông tin để debug
        print(f"Saving patient data: {patient_data}")

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
