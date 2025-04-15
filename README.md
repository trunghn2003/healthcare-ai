# Healthcare AI System

Hệ thống Healthcare AI sử dụng kiến trúc microservice và AI để hỗ trợ phân tích dữ liệu y tế, theo dõi và quản lý sức khỏe bệnh nhân.

## Kiến trúc hệ thống

Hệ thống bao gồm ba microservice chính:

1. **Gateway Service**: API Gateway cho phép truy cập vào các service khác qua một địa chỉ thống nhất.
2. **Patient Service**: Quản lý thông tin bệnh nhân và lịch sử chăm sóc sức khỏe.
3. **AI Service**: Cung cấp các dự đoán về nguy cơ bệnh dựa trên mô hình AI đã được huấn luyện.
4. **MongoDB**: Lưu trữ dữ liệu bệnh nhân và đánh giá sức khỏe.

## Yêu cầu hệ thống

- Docker và Docker Compose
- Python 3.9+
- Không gian đĩa tối thiểu 2GB để lưu trữ dữ liệu và mô hình AI

## Cách khởi động hệ thống

### Sử dụng Docker Compose

```bash
# Khởi động toàn bộ hệ thống
docker-compose up --build

# Khởi động ở chế độ nền
docker-compose up -d --build

# Dừng hệ thống
docker-compose down
```

### Khởi động từng service riêng biệt (chỉ dành cho phát triển)

```bash
# AI Service
cd services/ai_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002

# Patient Service
cd services/patient_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Gateway Service
cd services/gateway
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## API Endpoints

### Gateway API (http://localhost:8000)

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/patients` | GET | Lấy danh sách bệnh nhân |
| `/api/patients/{id}` | GET | Lấy thông tin bệnh nhân theo ID |
| `/api/patients` | POST | Tạo bệnh nhân mới |
| `/api/patients/{id}` | PUT | Cập nhật thông tin bệnh nhân |
| `/api/patients/{id}` | DELETE | Xóa bệnh nhân |
| `/api/predict` | POST | Dự đoán nguy cơ bệnh dựa trên mô hình AI |
| `/api/patients/{id}/health-assessment` | POST | Tạo đánh giá sức khỏe mới |
| `/api/patients/{id}/health-assessments` | GET | Lấy lịch sử đánh giá sức khỏe |
| `/api/health` | GET | Kiểm tra trạng thái của tất cả service |

### Mẫu dữ liệu

#### Tạo bệnh nhân mới
```json
{
  "name": "Nguyễn Văn A",
  "date_of_birth": "1985-05-15",
  "gender": "male",
  "contact": "0901234567",
  "medical_history": ["high blood pressure", "type 2 diabetes"]
}
```

#### Dự đoán nguy cơ bệnh
```json
{
  "features": [6.2, 148, 72, 35, 0, 33.6, 0.627, 50, 1, 1]
}
```

#### Tạo đánh giá sức khỏe
```json
{
  "features": [6.2, 148, 72, 35, 0, 33.6, 0.627, 50, 1, 1],
  "notes": "Bệnh nhân có dấu hiệu mệt mỏi, tăng khát nước",
  "recommendations": ["Giảm lượng đường tiêu thụ", "Tăng cường vận động"]
}
```

## Phát triển và mở rộng

### Thêm mô hình AI mới

1. Đào tạo mô hình sử dụng tập lệnh trong thư mục `ai_service/training`
2. Lưu mô hình đã đào tạo vào thư mục `ai_service/model`
3. Cập nhật API endpoints trong `ai_service/main.py` nếu cần

### Thêm service mới

1. Tạo thư mục mới trong `services/`
2. Thêm service vào `docker-compose.yml`
3. Cập nhật API Gateway để thêm routes đến service mới

## Xử lý sự cố

### MongoDB không kết nối được
- Kiểm tra xem container MongoDB đã chạy chưa: `docker ps`
- Kiểm tra logs: `docker-compose logs mongodb`

### AI Service không tải được mô hình
- Đảm bảo các file model đã được đặt trong thư mục `ai_service/model`
- Kiểm tra logs: `docker-compose logs ai-service`

## Đội ngũ phát triển

- Phát triển bởi: [Tên của bạn]
- Liên hệ: [Email của bạn]
