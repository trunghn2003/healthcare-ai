from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime
import sys
import os
from typing import List, Dict, Any

# Add parent directory to path for importing shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

app = FastAPI(title="Healthcare API Gateway",
              description="API Gateway for Healthcare AI System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs - sử dụng tên service trong docker-compose
PATIENT_SERVICE_URL = "http://patient-service:8000"
AI_SERVICE_URL = "http://ai-service:8000"

# Error handling middleware
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e), "timestamp": datetime.now().isoformat()}
        )

@app.get("/")
def read_root():
    return {
        "status": "Gateway is running",
        "version": "1.0.0",
        "services": {
            "patients": f"{PATIENT_SERVICE_URL}",
            "ai": f"{AI_SERVICE_URL}"
        }
    }

# Patient Service Routes
@app.get("/api/patients")
async def list_patients(skip: int = 0, limit: int = 10):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PATIENT_SERVICE_URL}/patients/", params={"skip": skip, "limit": limit})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.get("/api/patients/{patient_id}")
async def get_patient(patient_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PATIENT_SERVICE_URL}/patients/{patient_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.post("/api/patients", status_code=status.HTTP_201_CREATED)
async def create_patient(patient_data: Dict[str, Any]):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PATIENT_SERVICE_URL}/patients/", json=patient_data)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.put("/api/patients/{patient_id}")
async def update_patient(patient_id: str, patient_data: Dict[str, Any]):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{PATIENT_SERVICE_URL}/patients/{patient_id}", json=patient_data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.delete("/api/patients/{patient_id}")
async def delete_patient(patient_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{PATIENT_SERVICE_URL}/patients/{patient_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

# AI Service Routes
@app.post("/api/predict")
async def predict(data: Dict[str, Any]):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AI_SERVICE_URL}/predict", json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.post("/api/predict/disease")
async def predict_disease(data: Dict[str, Any]):
    return await predict(data)

# Integrated Endpoints
@app.post("/api/patients/{patient_id}/health-assessment")
async def create_health_assessment(patient_id: str, assessment_data: Dict[str, Any]):
    # First get prediction from AI service
    prediction_data = assessment_data.get("features")
    if not prediction_data:
        raise HTTPException(status_code=400, detail="Features data is required for assessment")

    # Get prediction from AI service
    async with httpx.AsyncClient() as client:
        prediction_response = await client.post(
            f"{AI_SERVICE_URL}/predict",
            json={"features": prediction_data}
        )

        if prediction_response.status_code != 200:
            raise HTTPException(
                status_code=prediction_response.status_code,
                detail=f"AI Service error: {prediction_response.text}"
            )

        prediction_result = prediction_response.json()

        # Create assessment data
        assessment = {
            "patient_id": patient_id,
            "disease_risk": prediction_result.get("disease_risk", "unknown"),
            "prediction_value": prediction_result.get("prediction", 0),
            "recommendations": assessment_data.get("recommendations", []),
            "notes": assessment_data.get("notes", "")
        }

        # Save assessment to patient service
        assessment_response = await client.post(
            f"{PATIENT_SERVICE_URL}/patients/{patient_id}/health-assessment",
            json=assessment
        )

        if assessment_response.status_code != 200:
            raise HTTPException(
                status_code=assessment_response.status_code,
                detail=f"Patient Service error: {assessment_response.text}"
            )

        # Return combined result
        return {
            "assessment_id": assessment_response.json().get("id"),
            "patient_id": patient_id,
            "prediction": prediction_result,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/patients/{patient_id}/health-assessments")
async def get_patient_assessments(patient_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PATIENT_SERVICE_URL}/patients/{patient_id}/health-assessments")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.get("/api/health")
async def health_check():
    """Check the health of all services"""
    results = {}

    async with httpx.AsyncClient() as client:
        # Check Gateway
        results["gateway"] = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }

        # Check Patient Service
        try:
            patient_response = await client.get(f"{PATIENT_SERVICE_URL}/health", timeout=2.0)
            results["patient_service"] = (
                patient_response.json() if patient_response.status_code == 200
                else {"status": "unhealthy", "code": patient_response.status_code}
            )
        except Exception as e:
            results["patient_service"] = {"status": "unhealthy", "error": str(e)}

        # Check AI Service
        try:
            ai_response = await client.get(f"{AI_SERVICE_URL}/health", timeout=2.0)
            results["ai_service"] = (
                ai_response.json() if ai_response.status_code == 200
                else {"status": "unhealthy", "code": ai_response.status_code}
            )
        except Exception as e:
            results["ai_service"] = {"status": "unhealthy", "error": str(e)}

    # Overall status
    all_healthy = all(service["status"] == "healthy" for service in results.values())
    results["overall"] = "healthy" if all_healthy else "degraded"

    return results
