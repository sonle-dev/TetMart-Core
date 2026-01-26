from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# 1. TẠO KHO DỮ LIỆU GIẢ (MOCK DATA)
products_data = [
    {
        'id': 1,
        'name': 'Đèn lồng đỏ truyền thống',
        'price': '150.000',
        'image': 'https://salt.tikicdn.com/cache/750x750/ts/product/d0/20/7a/12a86847c2310137452d921356247c18.jpg.webp',
        'category': 'Đèn lồng',
        'icon': '🏮',
        'desc': 'Đèn lồng vải nhung đỏ thắm, khung thép chắc chắn, mang lại may mắn.'
    },
    {
        'id': 2,
        'name': 'Cành hoa mai vàng',
        'price': '180.000',
        'image': 'https://bizweb.dktcdn.net/100/443/076/products/trang-tri-tet-hoa-dao-dong.jpg',
        'category': 'Hoa mai/đào',
        'icon': '🌸',
        'desc': 'Cành hoa mai giả cao cấp, màu sắc tươi tắn, bền đẹp suốt mùa Tết.'
    },
    {
        'id': 3,
        'name': 'Bao lì xì hoa mai vàng',
        'price': '25.000',
        'image': 'https://salt.tikicdn.com/cache/w1200/ts/product/6e/c8/10/7c462744d03d09a06655c65b5302636a.jpg',
        'category': 'Bao lì xì',
        'icon': '🧧',
        'desc': 'Combo 10 bao lì xì giấy cứng, in họa tiết rồng vàng sang trọng.'
    },
    {
        'id': 4,
        'name': 'Dây treo chữ Phúc',
        'price': '45.000',
        'image': 'https://vn-test-11.slatic.net/p/3c73499427b20387498c89599d14620f.jpg',
        'category': 'Dây trang trí',
        'icon': '🎊',
        'desc': 'Dây treo trang trí cửa nhà, mang ý nghĩa Phúc Lộc Thọ toàn gia.'
    }
]

# Hàm hiển thị trang chủ
def index(request):
    return render(request, 'index.html')

# Hàm hiển thị chi tiết sản phẩm
def product_detail(request, product_id):
    product = None
    for item in products_data:
        if item['id'] == product_id:
            product = item
            break
    
    context = {'product': product}
    return render(request, 'product_detail.html', context)

# ---------------------------------------------------------
# CÁC HÀM XỬ LÝ TÀI KHOẢN (Auth)
# ---------------------------------------------------------

def register_view(request):
    """Trang Đăng ký"""
    if request.method == 'POST':
        # Logic lưu vào DB sẽ viết ở đây sau
        
        # Thông báo thành công
        messages.success(request, 'Đăng ký tài khoản thành công! Vui lòng đăng nhập.')
        return redirect('core:login')

    # 👇 ĐÃ SỬA: Trỏ vào thư mục user/register.html
    return render(request, 'user/register.html')


def login_view(request):
    """Trang Đăng nhập"""
    if request.method == 'POST':
        # 1. Lấy dữ liệu từ form
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        # 2. Kiểm tra xác thực
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            # ✅ Đăng nhập thành công
            login(request, user)
            messages.success(request, f"Chào mừng {user.username} quay trở lại!")
            
            # Kiểm tra xem người dùng có đang muốn vào trang nào trước đó không (ví dụ Dashboard)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
        else:
            # ❌ Đăng nhập thất bại
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
            
    # 👇 ĐÃ SỬA: Trỏ vào thư mục user/login.html
    return render(request, 'user/login.html')


def logout_view(request):
    """Xử lý Đăng xuất"""
    logout(request)
    messages.success(request, "Đăng xuất thành công! Hẹn gặp lại. 👋")
    return redirect('core:login')