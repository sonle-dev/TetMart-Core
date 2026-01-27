from django.shortcuts import render, get_object_or_404, redirect # 👈 Đã thêm redirect
from django.contrib import messages # 👈 Đã thêm messages để hiện thông báo
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
    # Tìm sản phẩm trong danh sách dựa vào ID
    product = None
    for item in products_data:
        if item['id'] == product_id:
            product = item
            break
    
    context = {'product': product}
    return render(request, 'product_detail.html', context)

# Hàm hiển thị trang đăng nhập
def login_view(request):
    # Nếu bấm nút Đăng nhập (POST), bạn có thể xử lý ở đây sau
    if request.method == 'POST':
        # Tạm thời chưa xử lý logic thật, chỉ render lại trang
        pass
    return render(request, 'login.html')

# Hàm hiển thị trang đăng ký (ĐÃ SỬA LOGIC THÔNG BÁO)
def register_view(request):
    # Kiểm tra nếu người dùng bấm nút Submit (Gửi form)
    if request.method == 'POST':
        # 1. (Sau này logic lưu vào DB sẽ nằm ở đây)
        
        # 2. Tạo thông báo thành công màu xanh
        messages.success(request, '🎉 Đăng ký tài khoản thành công! Vui lòng đăng nhập.')
        
        # 3. Chuyển hướng người dùng sang trang Đăng nhập
        return redirect('core:login')

    # Nếu vào bình thường (GET) thì hiện form đăng ký
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        # 1. Lấy dữ liệu từ ô input (nhờ vào cái name="username" ta vừa thêm)
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        # 2. Kiểm tra thông tin đăng nhập
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            # ✅ ĐÚNG: Đăng nhập và chuyển về trang chủ
            login(request, user)
            messages.success(request, f"🎉 Chào mừng {user.username} quay trở lại!")
            return redirect('core:home')
        else:
            # ❌ SAI: Bắn thông báo lỗi
            messages.error(request, "⚠️ Tên đăng nhập hoặc mật khẩu không đúng!")
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request) # Xóa phiên đăng nhập
    messages.success(request, "👋 Đăng xuất thành công! Hẹn gặp lại.")
    return redirect('core:login') # Chuyển hướng về trang đăng nhập
@login_required(login_url='core:login')
def dashboard_view(request):
    # Dữ liệu giả để test giao diện
    context = {
        'total_orders': 150,
        'revenue': '25.000.000',
        'pending_orders': 5,
        'total_products': 48
    }
    return render(request, 'dashboard.html', context)