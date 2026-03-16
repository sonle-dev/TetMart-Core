🧨 TetMart – Hệ thống Quản lý Bán hàng & Kho vận

Tech Lead: Lê Hồng Sơn
Thành viên: Nguyễn Danh Thế, Ngô Thị Sinh
Nhánh phát triển chính: main

Dự án xây dựng hệ thống quản lý bán hàng Tết, tập trung vào việc xử lý số liệu backend, thống kê báo cáo và quản lý trạng thái đơn hàng theo thời gian thực.

🚀 1. Các tính năng đã hoàn thiện (Done)

Dựa trên yêu cầu của Bài kiểm tra kỹ năng 3, nhóm đã hoàn thiện các chức năng chính sau:

1.1 CRUD cho các bảng dữ liệu chính

Hệ thống đã triển khai đầy đủ chức năng:

Thêm – Xem – Sửa – Xóa (CRUD) cho các bảng dữ liệu chính trong hệ thống:

Product – Quản lý thông tin sản phẩm

Order – Quản lý đơn hàng

OrderDetail – Chi tiết đơn hàng

Customer/User – Quản lý người dùng

Các thao tác CRUD được xây dựng thông qua Django Views kết hợp với Template, đảm bảo việc quản lý dữ liệu diễn ra thuận tiện và chính xác.

1.2 Chức năng tìm kiếm, lọc và sắp xếp dữ liệu

Hệ thống hỗ trợ các chức năng giúp người dùng dễ dàng tìm kiếm và quản lý dữ liệu:

Tìm kiếm sản phẩm theo tên sản phẩm

Lọc sản phẩm theo danh mục

Sắp xếp dữ liệu theo:

giá

tên

thời gian

Các chức năng này giúp cải thiện trải nghiệm người dùng khi làm việc với hệ thống quản lý sản phẩm và đơn hàng.

1.3 Phân quyền người dùng (Guest / User / Admin)

Hệ thống triển khai cơ chế phân quyền dựa trên hệ thống Authentication của Django.

Vai trò	Quyền
Guest	Xem thông tin sản phẩm
User	Đặt hàng, quản lý giỏ hàng
Admin	Quản lý sản phẩm, đơn hàng và người dùng

Cơ chế phân quyền giúp đảm bảo mỗi người dùng chỉ truy cập được các chức năng phù hợp với quyền hạn của mình.

1.4 Xử lý luồng nghiệp vụ đặt hàng

Hệ thống xây dựng luồng nghiệp vụ đặt hàng gồm các bước:

Người dùng đăng nhập vào hệ thống

Chọn sản phẩm cần mua

Thêm sản phẩm vào giỏ hàng

Tiến hành đặt hàng

Quản trị viên xử lý đơn hàng

Luồng nghiệp vụ này mô phỏng quá trình hoạt động của một hệ thống thương mại điện tử thực tế.

1.5 Trạng thái dữ liệu

Hệ thống sử dụng các trạng thái dữ liệu để quản lý tiến trình xử lý đơn hàng:

pending – chờ xử lý

approved – đã duyệt

rejected – từ chối

active / inactive – trạng thái hoạt động của dữ liệu

Nhờ đó quản trị viên có thể dễ dàng theo dõi tình trạng xử lý của từng đơn hàng.

1.6 Upload hình ảnh / tệp

Hệ thống cho phép tải lên hình ảnh sản phẩm khi thêm hoặc chỉnh sửa dữ liệu.

Các tệp tải lên được kiểm tra:

Định dạng file

Kích thước file

nhằm đảm bảo tính an toàn và ổn định cho hệ thống.

1.7 Hiển thị thông báo hệ thống

Hệ thống sử dụng alert / toast notification để hiển thị thông báo khi người dùng thực hiện các thao tác:

Thêm dữ liệu thành công

Cập nhật dữ liệu

Xóa dữ liệu

Thông báo lỗi khi thao tác thất bại

Nhờ đó người dùng có thể dễ dàng nhận biết kết quả của các thao tác trên hệ thống.

1.8 Kiến trúc hệ thống

Dự án được xây dựng theo kiến trúc MVT (Model – View – Template) của Django.

Cấu trúc code được tổ chức thành nhiều apps riêng biệt:

products

orders

users

dashboard

Mỗi module đều được tổ chức theo cấu trúc chuẩn của Django:

models.py
views.py
urls.py
admin.py
1.9 Kiểm thử hệ thống

Các chức năng chính đã được kiểm thử thủ công để đảm bảo hệ thống hoạt động ổn định:

CRUD sản phẩm

Tìm kiếm sản phẩm

Đặt hàng

Phân quyền người dùng

Kết quả kiểm thử cho thấy hệ thống hoạt động đúng theo yêu cầu đề bài.

1.10 Quản lý mã nguồn bằng GitHub

Toàn bộ mã nguồn được quản lý thông qua Git và GitHub.

Nhóm sử dụng mô hình làm việc theo branch:

Mỗi thành viên phát triển trên một nhánh riêng

Sau đó merge vào nhánh main

Repository dự án:

https://github.com/sonle-dev/TetMart-Core

Trong quá trình phát triển, nhóm đã thực hiện hơn 10 commit để ghi nhận tiến độ phát triển của hệ thống.

🛠 2. Yêu cầu cài đặt (Dành cho Giảng viên / Tester)

⚠ Vì dự án sử dụng MySQL và code mới nhất nằm ở nhánh main, vui lòng làm đúng các bước sau.

Bước 1: Lấy code về máy
# Clone dự án
git clone https://github.com/sonle-dev/TetMart-Core.git

# Di chuyển vào thư mục
cd TetMart-Core

# Chuyển sang nhánh main
git checkout main
Bước 2: Thiết lập môi trường Python
# Tạo môi trường ảo
py -m venv venv

# Kích hoạt môi trường ảo
venv\Scripts\Activate.ps1

# Cài đặt thư viện
pip install -r requirements.txt
Bước 3: Khôi phục dữ liệu MySQL

Dự án đã có dữ liệu demo trong file backup.

1. Tạo Database

Mở MySQL Workbench hoặc phpMyAdmin
Tạo database:

tet_mart_db
2. Import dữ liệu

Tìm file:

database_backup.sql

Import file này vào database vừa tạo.

3. Cấu hình kết nối database

Mở file:

tetmart/settings.py

Tìm phần:

DATABASES

và chỉnh lại PASSWORD cho đúng với máy của bạn.

Bước 4: Chạy Server
python manage.py runserver

Truy cập:

http://127.0.0.1:8000/
🔐 3. Tài khoản Demo

Sau khi import SQL thành công:

Tài khoản Admin

Username: admin

Password: 123

Tài khoản User

Username: user1

Password: 123456a@

📂 4. Cấu trúc dự án

products/        # Xử lý logic sản phẩm

orders/          # Xử lý đơn hàng và giỏ hàng

tetmart/         # Cấu hình chính (Settings, URLs)

templates/       # Giao diện HTML

static/          # CSS, JS, Images

database_backup.sql

🎥 5. Video Demo Hệ Thống

https://github.com/user-attachments/assets/d966ce9f-83a9-4e93-8bb5-229d570e2