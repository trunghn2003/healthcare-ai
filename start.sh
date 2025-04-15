#!/bin/bash

# Đảm bảo shared directory có thể được import
mkdir -p shared/models
mkdir -p shared/utils

# Khởi động hệ thống với Docker Compose
echo "Khởi động Healthcare AI System..."
docker-compose up --build

# Lưu ý: Nhấn Ctrl+C để dừng hệ thống
