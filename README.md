# 🧨 TetMart - Hệ thống Quản lý Bán hàng & Kho vận

> **Tech Lead:** Lê Hồng Sơn
**member:** Nguyễn Danh Thế, Ngô Thị Sinh
> **Nhánh phát triển chính:** `main`

 Dự án xây dựng hệ thống quản lý bán hàng Tết,   tập trung vào việc xử lý số liệu backend, thống kê báo cáo và quản lý trạng thái đơn hàng theo thời gian thực.

## 🚀 1. Các tính năng đã hoàn thiện (Done)

 Dựa trên yêu cầu bài toán, nhóm đã hoàn thành và tích hợp các module sau:

### 🔹 Phần Backend (Django Core)
* **Quản trị hệ thống:** Đăng nhập, Phân quyền Admin/Staff.

* **Dashboard (Bảng điều khiển):**
    * Hiển thị **số liệu thực** từ Database (Tổng doanh thu, Tổng đơn hàng).
    * Tích hợp logic tính toán doanh thu theo thời gian.
    
* **Module Báo cáo (Report):**
    Xây dựng View xử lý dữ liệu báo cáo.  
 **Database:**
   Chuyển đổi thành công từ SQLite sang **MySQL**.
   Thiết kế Schema chuẩn: Bảng `Product`, `Order`, `OrderDetail`, `Customer`.

### 🔹 Phần Frontend (Giao diện)
     Đã ghép nối hoàn chỉnh giao diện HTML/CSS vào Django Template.

* **Các trang đã chạy mượt:**
   * Trang chủ Dashboard (Biểu đồ, Thống kê).
    Danh sách đơn hàng (Trạng thái màu sắc trực quan).
    * Chi tiết sản phẩm.

## 🛠 2. Yêu cầu cài đặt (Dành cho Giảng viên/Tester)

 Vì dự án sử dụng **MySQL** và **Code mới nhất nằm ở nhánh `main`**, vui lòng làm đúng các bước sau để tránh lỗi.

### Bước 1: Lấy code về máy

# Clone dự án
 git clone https://github.com/sonle-dev/TetMart-Core.git

# Di chuyển vào thư mục
 cd TetMart-Core

# CHUYỂN SANG NHÁNH MAIN (Code hoàn chỉnh ở đây)
 git checkout main

### Bước 2: Thiết lập môi trường Python

# 1. Tạo môi trường ảo
 py -m venv venv

# 2. Kích hoạt môi trường ảo
 venv\Scripts\Activate.ps1

# 3. Cài đặt thư viện
 pip install -r requirements.txt

### Bước 3: Khôi phục Dữ liệu (MySQL) ⚠️
 Dự án đã có sẵn dữ liệu demo (Sản phẩm, Đơn hàng, User Admin) trong file backup.

1.	Tạo Database: Mở Workbench hoặc phpMyAdmin 
    tạo DB tên: tet_mart_db

2.	Import Dữ liệu:
	Tìm file: database_backup.sql (nằm ngay thư mục gốc dự án).
	Import file này vào database vừa tạo.

3.	Cấu hình kết nối:
	Mở file: tetmart/settings.py
	Tìm đoạn DATABASES, sửa lại PASSWORD cho đúng với máy của bạn.

### Bước 4: Chạy Server
    python manage.py runserver
    Truy cập: http://127.0.0.1:8000/

## 🔐 3. Tài khoản Demo
 Sau khi Import file SQL thành công, sử dụng tài khoản sau:
### Tài khoản Admin:
	Username: admin
	Password: 123
### Tài khoản user:
	Username: user1
	Password: 123456a@

## 📂 4. Cấu trúc dự án
    - products/: Xử lý logic sản phẩm.
    - orders/: Xử lý đơn hàng và giỏ hàng.
	- tetmart/: Cấu hình chính (Settings, URLs).
	- templates/: Chứa file giao diện HTML (Dashboard, Base layout...).
	- static/: Chứa CSS, JS, Images.
	- database_backup.sql: File backup dữ liệu MySQL trọn gói.

## 5. Link Video Demo Trang Web Trang Web Đến Thời Điểm Hiện Tại 

https://github.com/user-attachments/assets/d966ce9f-83a9-4e93-8bb5-229d570e2c57


