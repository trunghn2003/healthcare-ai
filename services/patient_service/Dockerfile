FROM python:3.9-slim

WORKDIR /app

# Cài đặt các gói
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY . .

# Expose port cho FastAPI
EXPOSE 8000

# Command để chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
