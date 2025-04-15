# training/train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import joblib
import os

# Tạo thư mục model
os.makedirs('../model', exist_ok=True)


def load_and_prepare_data():
    # Load diabetes dataset
    df = pd.read_csv('data/diabetes.csv')

    # Normalize target variable (vì đây là regression problem)
    target_mean = df['target'].mean()
    target_std = df['target'].std()
    df['target'] = (df['target'] - target_mean) / target_std

    X = df.drop('target', axis=1).values
    y = df['target'].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def create_model(input_dim):
    model = Sequential([
        Dense(128, activation='relu', input_dim=input_dim),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)  # Linear activation for regression
    ])

    optimizer = Adam(learning_rate=0.001)

    model.compile(
        optimizer=optimizer,
        loss='mse',  # Mean Squared Error for regression
        metrics=['mae']  # Mean Absolute Error
    )

    return model


def train_model():
    # Load and prepare data
    X_train, X_test, y_train, y_test, scaler = load_and_prepare_data()

    # Create callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )

    model_checkpoint = ModelCheckpoint(
        '../model/best_model.keras',
        monitor='val_loss',
        save_best_only=True
    )

    # Create and train model
    model = create_model(X_train.shape[1])

    print("Training model...")
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=100,
        batch_size=32,
        callbacks=[early_stopping, model_checkpoint],
        verbose=1
    )

    # Save scaler
    joblib.dump(scaler, '../model/scaler.pkl')

    # Evaluate model
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nTest Loss (MSE): {test_loss:.4f}")
    print(f"Test MAE: {test_mae:.4f}")

    return model, scaler, history


def plot_history(history):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 4))

    # Plot loss
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plot MAE
    plt.subplot(1, 2, 2)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.title('Model MAE')
    plt.xlabel('Epoch')
    plt.ylabel('MAE')
    plt.legend()

    plt.tight_layout()
    plt.savefig('../model/training_history.png')
    plt.close()


if __name__ == "__main__":
    # Train model
    model, scaler, history = train_model()

    # Plot training history
    plot_history(history)

    # Test prediction
    sample_data = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
    scaled_sample = scaler.transform(sample_data)
    prediction = model.predict(scaled_sample)
    print(f"\nSample prediction: {prediction[0][0]:.4f}")
