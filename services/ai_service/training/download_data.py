# training/download_data.py
import pandas as pd
from sklearn.datasets import load_diabetes

# Tạo dữ liệu mẫu
def create_sample_data():
    # Load diabetes dataset
    diabetes = load_diabetes()
    df = pd.DataFrame(
        data=diabetes.data,
        columns=diabetes.feature_names
    )
    df['target'] = diabetes.target

    # Lưu file
    df.to_csv('data/diabetes.csv', index=False)

if __name__ == "__main__":
    create_sample_data()
