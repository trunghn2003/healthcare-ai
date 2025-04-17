from django import forms
from datetime import date

class PatientForm(forms.Form):
    # Thông tin cá nhân
    full_name = forms.CharField(
        label='Họ và tên',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        label='Ngày sinh',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    gender = forms.ChoiceField(
        label='Giới tính',
        choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Khác', 'Khác')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Số điện thoại',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Địa chỉ',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Thông tin y tế
    pregnancies = forms.IntegerField(
        label='Số lần mang thai',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    glucose = forms.FloatField(
        label='Nồng độ glucose',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    blood_pressure = forms.FloatField(
        label='Huyết áp',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    skin_thickness = forms.FloatField(
        label='Độ dày nếp gấp da',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    insulin = forms.FloatField(
        label='Insulin',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bmi = forms.FloatField(
        label='Chỉ số BMI',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    diabetes_pedigree_function = forms.FloatField(
        label='Hàm phả hệ tiểu đường',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        label='Tuổi',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
