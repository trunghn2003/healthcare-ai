import pandas as pd
import urllib.request
import os

def download_diabetes_data():
    # URL của dataset Pima Indians Diabetes
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    
    # Tạo thư mục data nếu chưa tồn tại
    os.makedirs('data', exist_ok=True)
    
    # Download dataset
    print("Đang tải dataset...")
    urllib.request.urlretrieve(url, 'data/diabetes.csv')
    
    # Đọc và thêm tên cột
    column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                   'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    
    df = pd.read_csv('data/diabetes.csv', names=column_names)
    
    # Lưu lại file với tên cột
    df.to_csv('data/diabetes.csv', index=False)
    print("Đã tải và cập nhật dataset thành công!")
    
    # Hiển thị thông tin cơ bản về dataset
    print("\nThông tin về dataset:")
    print(df.info())
    print("\nMẫu dữ liệu:")
    print(df.head())

if __name__ == "__main__":
    download_diabetes_data()
