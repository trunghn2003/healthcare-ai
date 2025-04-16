from fastapi import FastAPI, HTTPException
import numpy as np
import tensorflow as tf
import joblib
from shared.models.patient import PatientBase
import os

app = FastAPI()

# Load model and scaler
model_path = os.path.join(os.path.dirname(__file__), "model/best_model.keras")
scaler_path = os.path.join(os.path.dirname(__file__), "model/scaler.pkl")

try:
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    raise

@app.post("/predict")
async def predict_diabetes(patient: PatientBase):
    try:
        # Convert patient data to numpy array
        features = np.array([[
            patient.pregnancies,
            patient.glucose,
            patient.blood_pressure,
            patient.skin_thickness,
            patient.insulin,
            patient.bmi,
            patient.diabetes_pedigree_function,
            patient.age
        ]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)[0][0]

        return {
            "diabetes_prediction": float(prediction),
            "is_diabetic": bool(prediction > 0.5)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
