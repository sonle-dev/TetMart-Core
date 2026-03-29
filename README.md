# TetMart Core

TetMart Core là hệ thống web thương mại điện tử mini chuyên cung cấp các sản phẩm trang trí Tết. Dự án được xây dựng bằng Django với kiến trúc module hóa, phục vụ mục đích học tập và phát triển thực tế theo mô hình backend – frontend.


## 1. Giới thiệu

Hệ thống bao gồm hai nhóm người dùng chính:

- Người dùng: xem sản phẩm, đăng ký, đăng nhập, thêm giỏ hàng và đặt hàng  
- Quản trị viên: quản lý sản phẩm, đơn hàng và theo dõi báo cáo thống kê  

Dự án được thiết kế theo hướng dễ mở rộng, rõ ràng về cấu trúc và phù hợp với workflow làm việc nhóm.


## 2. Tính năng

### Người dùng
- Đăng ký, đăng nhập, đăng xuất  
- Xem danh sách sản phẩm  
- Xem chi tiết sản phẩm  
- Thêm sản phẩm vào giỏ hàng  
- Đặt hàng  

### Quản trị
- Dashboard tổng quan  
- Quản lý sản phẩm  
- Quản lý đơn hàng  
- Cập nhật trạng thái đơn hàng  
- Thống kê và báo cáo doanh thu  


## 3. Công nghệ sử dụng

### Backend
- Python  
- Django  

### Frontend
- HTML, CSS  
- Bootstrap  
- JavaScript  

### Database
- MySQL  

### Thư viện
- Django  
- PyMySQL  
- Pillow  
- python-dotenv  


## 4. Kiến trúc dự án


TetMart-Core/
├── products/
├── orders/
├── users/
├── templates/
├── static/
├── tetmart/


Luồng hoạt động:


User → View → Model → Database


## 5. Cài đặt

### 5.1 Clone repository

```bash
git clone https://github.com/sonle-dev/TetMart-Core.git
cd TetMart-Core
5.2 Tạo môi trường ảo

Windows:

python -m venv .venv
.venv\Scripts\activate

Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

5.3 Cài đặt dependencies
pip install -r requirements.txt

6. Cấu hình database

Tạo database:

CREATE DATABASE tet_mart_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Cập nhật trong tetmart/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tet_mart_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

7. Khởi tạo dữ liệu
python manage.py makemigrations
python manage.py migrate

Hoặc import:

mysql -u your_user -p tet_mart_db < database_backup.sql

8. Chạy dự án
python manage.py runserver

Truy cập:

http://127.0.0.1:8000/

9. Tài khoản
Quản trị
python manage.py createsuperuser

Truy cập:

http://127.0.0.1:8000/admin/
Người dùng
Đăng ký: /auth/register/
Đăng nhập: /auth/login/

10. Git Workflow

Các nhánh sử dụng:

main
develop
feature/backend
feature/frontend
feature/tester

Quy trình:

feature → develop → main

Ví dụ commit:

git commit -m "fix(auth): sửa lỗi login/register không nhận dữ liệu"

11. Đóng góp
git checkout -b feature/your-feature
git commit -m "feat: thêm chức năng ..."
git push origin feature/your-feature

Sau đó tạo Pull Request.

12. Lưu ý
Không commit file .env
Không push dữ liệu database thật
Kiểm tra migration trước khi push

13. Tác giả

Lê Hồng Sơn
Nguyễn Danh Thế
Ngô Thị Sinh

14. Giấy phép

Dự án phục vụ mục đích học tập và phát triển nội bộ.