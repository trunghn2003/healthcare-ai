"""
Utility functions for healthcare-ai system
"""
import numpy as np
from datetime import datetime


def calculate_risk_level(prediction_value: float) -> str:
    """
    Calculate risk level based on prediction value

    Args:
        prediction_value: Prediction value from model (0-1)

    Returns:
        Risk level as string: 'low', 'medium', or 'high'
    """
    if prediction_value < 0.3:
        return "low"
    elif prediction_value < 0.7:
        return "medium"
    else:
        return "high"


def generate_recommendations(prediction_value: float, risk_level: str) -> list:
    """
    Generate health recommendations based on prediction and risk level

    Args:
        prediction_value: Prediction value from model
        risk_level: Risk level ('low', 'medium', 'high')

    Returns:
        List of recommendation strings
    """
    recommendations = []

    # Common recommendations for all risk levels
    recommendations.append("Maintain a balanced diet rich in fruits and vegetables")
    recommendations.append("Get regular physical activity (at least 150 minutes/week)")
    recommendations.append("Ensure adequate sleep (7-9 hours per night)")

    # Risk-specific recommendations
    if risk_level == "medium":
        recommendations.append("Schedule a follow-up appointment within 3 months")
        recommendations.append("Monitor your health metrics weekly")
    elif risk_level == "high":
        recommendations.append("Schedule a comprehensive check-up within 1 month")
        recommendations.append("Consider consultation with a specialist")
        recommendations.append("Follow a strict monitoring schedule as advised by your doctor")

    return recommendations


def format_datetime(dt: datetime) -> str:
    """Format datetime object to string"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")
