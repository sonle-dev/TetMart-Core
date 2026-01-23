from django.shortcuts import render

# Hàm hiển thị trang chủ
def index(request):
    # Nó sẽ tự tìm file index.html trong thư mục templates bạn vừa tạo
    return render(request, 'index.html')