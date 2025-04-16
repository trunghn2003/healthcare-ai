from django import forms

class DiabetesPredictionForm(forms.Form):
    pregnancies = forms.IntegerField(label='Số lần mang thai', min_value=0)
    glucose = forms.FloatField(label='Nồng độ glucose', min_value=0)
    blood_pressure = forms.FloatField(label='Huyết áp tâm trương (mm Hg)', min_value=0)
    skin_thickness = forms.FloatField(label='Độ dày nếp gấp da (mm)', min_value=0)
    insulin = forms.FloatField(label='Insulin (mu U/ml)', min_value=0)
    bmi = forms.FloatField(label='Chỉ số BMI', min_value=0)
    diabetes_pedigree_function = forms.FloatField(label='Hàm phả hệ tiểu đường', min_value=0)
    age = forms.IntegerField(label='Tuổi', min_value=0)
