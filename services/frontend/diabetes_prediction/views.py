from django.shortcuts import render
import requests
import os
import json
from .forms import PatientForm

# API Gateway URL - lấy từ environment hoặc sử dụng default
GATEWAY_URL = os.environ.get('GATEWAY_URL', 'http://localhost:8000')

def home(request):
    form = PatientForm()
    prediction_result = None

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            try:
                # Lấy dữ liệu từ form
                form_data = form.cleaned_data

                # Chuyển date_of_birth sang định dạng ISO để có thể serialize với JSON
                if 'date_of_birth' in form_data and form_data['date_of_birth']:
                    form_data['date_of_birth'] = form_data['date_of_birth'].isoformat()

                # In dữ liệu gửi đi để debug
                print(f"Sending data to API: {form_data}")

                # Gửi dữ liệu đến Gateway API
                response = requests.post(
                    f"{GATEWAY_URL}/api/predict",
                    json=form_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5  # Thêm timeout để tránh treo quá lâu
                )

                # In thông tin response để debug
                print(f"API response status: {response.status_code}")
                print(f"API response content: {response.text}")

                response.raise_for_status()
                prediction_result = response.json()

                # Chuyển đổi xác suất về dạng phần trăm để hiển thị
                if 'diabetes_prediction' in prediction_result:
                    prediction_result['diabetes_prediction'] = prediction_result['diabetes_prediction'] * 100

            except requests.exceptions.RequestException as e:
                error_msg = f"Lỗi kết nối đến API: {str(e)}"
                print(f"API connection error: {error_msg}")
                prediction_result = {"error": error_msg}
            except Exception as e:
                error_msg = f"Lỗi: {str(e)}"
                print(f"General error: {error_msg}")
                prediction_result = {"error": error_msg}
        else:
            # Thêm xử lý khi form không hợp lệ
            print(f"Form errors: {form.errors}")
            prediction_result = {"error": "Dữ liệu nhập vào không hợp lệ. Vui lòng kiểm tra lại."}

    return render(request, 'diabetes_prediction/home.html', {
        'form': form,
        'prediction_result': prediction_result
    })

def patient_list(request):
    patients = []
    error_message = None

    try:
        # Lấy dữ liệu bệnh nhân từ Gateway API
        response = requests.get(f"{GATEWAY_URL}/api/patients", timeout=3)  # Thêm timeout
        response.raise_for_status()
        patients = response.json()

        # Chuyển đổi xác suất về dạng phần trăm để hiển thị
        for patient in patients:
            if 'diabetes_prediction' in patient:
                patient['diabetes_prediction'] = patient['diabetes_prediction'] * 100

    except requests.exceptions.RequestException as e:
        error_message = f"Không thể kết nối đến API Gateway. Vui lòng đảm bảo rằng dịch vụ backend đang chạy. Lỗi: {str(e)}"
        print(f"Lỗi kết nối đến API: {str(e)}")
    except Exception as e:
        error_message = f"Đã xảy ra lỗi: {str(e)}"
        print(f"Lỗi: {str(e)}")

    return render(request, 'diabetes_prediction/patient_list.html', {
        'patients': patients,
        'error_message': error_message
    })
