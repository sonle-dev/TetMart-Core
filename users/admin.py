from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Tạo class quản lý User riêng để hiện thêm cột số điện thoại, địa chỉ
class CustomUserAdmin(UserAdmin):
    model = User
    # 1. Các cột hiển thị ở danh sách danh sách
    list_display = ['username', 'email', 'phone', 'is_customer', 'is_staff']
    
    # 2. Form nhập liệu (Thêm các trường mới vào form mặc định)
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin thêm', {'fields': ('phone', 'address', 'avatar', 'is_customer')}),
    )

# Đăng ký vào Admin
admin.site.register(User, CustomUserAdmin)