# training/test_model.py
import tensorflow as tf
import joblib
import numpy as np


def test_saved_model():
    # Load model và scaler
    model = tf.keras.models.load_model('../model/best_model.keras')
    scaler = joblib.load('../model/scaler.pkl')

    # Tạo dữ liệu test
    sample_data = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ])

    # Scale dữ liệu
    scaled_data = scaler.transform(sample_data)

    # Predict
    predictions = model.predict(scaled_data)

    print("\nTest Predictions:")
    for i, pred in enumerate(predictions):
        print(f"Sample {i + 1}: {pred[0]:.4f}")


if __name__ == "__main__":
    test_saved_model()
