from django.shortcuts import render
from django.conf import settings
import requests
from .forms import DiabetesPredictionForm

def home(request):
    prediction_result = None
    if request.method == 'POST':
        form = DiabetesPredictionForm(request.POST)
        if form.is_valid():
            # Gửi dữ liệu đến API Gateway
            try:
                response = requests.post(
                    f"{settings.SERVICES['GATEWAY_URL']}/api/patients/",
                    json=form.cleaned_data
                )
                response.raise_for_status()
                prediction_result = response.json()
            except requests.exceptions.RequestException as e:
                prediction_result = {"error": str(e)}
    else:
        form = DiabetesPredictionForm()

    return render(request, 'diabetes_prediction/home.html', {
        'form': form,
        'prediction_result': prediction_result
    })

def patient_list(request):
    try:
        response = requests.get(f"{settings.SERVICES['GATEWAY_URL']}/api/patients/")
        response.raise_for_status()
        patients = response.json()
    except requests.exceptions.RequestException:
        patients = []

    return render(request, 'diabetes_prediction/patient_list.html', {
        'patients': patients
    })
