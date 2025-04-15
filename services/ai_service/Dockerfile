FROM python:3.9-slim

WORKDIR /app

# Cài đặt các dependency cần thiết để build numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Cython trước
RUN pip install --no-cache-dir Cython==0.29.24

# Cài đặt numpy trước với phiên bản cụ thể
RUN pip install --no-cache-dir numpy==1.19.5

# Sau đó cài đặt các dependency còn lại
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY . .

# Tạo thư mục model nếu chưa tồn tại
RUN mkdir -p /app/model

# Expose port cho FastAPI
EXPOSE 8000

# Command để chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
