from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
import json

# Import Form tùy chỉnh của bạn
from .forms import CustomUserCreationForm 

# Import Model Order
from orders.models import Order 

# --- 1. LOGIC ĐĂNG KÝ (Đã sửa chuẩn) ---
def register_view(request):
    if request.method == 'POST':
        # 👇 ĐÃ SỬA: Dùng CustomUserCreationForm thay vì UserCreationForm
        form = CustomUserCreationForm(request.POST) 
        
        if form.is_valid():
            user = form.save() 
            login(request, user) # Đăng nhập luôn sau khi đăng ký
            messages.success(request, f"Chào mừng {user.username} đến với TetMart!")
            return redirect('home') 
        else:
            # Nếu form lỗi (vd: mật khẩu không khớp), in lỗi ra
            messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.")
    else:
        # 👇 ĐÃ SỬA: Dùng CustomUserCreationForm tạo form rỗng
        form = CustomUserCreationForm()
    
    # 👇 QUAN TRỌNG: Dòng này nằm ngoài cùng, thẳng hàng với if/else
    return render(request, 'users/register.html', {'form': form})

# --- 2. LOGIC ĐĂNG NHẬP ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            messages.success(request, f"Chào mừng {user.username} quay trở lại!")
            
            # Nếu là Staff thì chuyển thẳng vào Dashboard
            if user.is_staff:
                return redirect('dashboard')
            return redirect('home')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

# --- 3. LOGIC ĐĂNG XUẤT ---
def logout_view(request):
    logout(request)
    messages.info(request, "Đã đăng xuất thành công.") 
    return redirect('login') 

# --- HÀM KIỂM TRA QUYỀN (Helper) ---
def is_staff(user):
    return user.is_staff

# --- 4. DASHBOARD ---
@login_required
@user_passes_test(is_staff) 
def dashboard_view(request):
    context = {
        'revenue': "15.000.000", 
        'count_new': 5,
        'count_processing': 2,
        'count_shipping': 1,
        'count_completed': 10,
        'count_cancelled': 0,
    }
    return render(request, 'dashboard.html', context)

# --- 5. DANH SÁCH ĐƠN HÀNG ---
@login_required
@user_passes_test(is_staff)
def order_list_view(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)

# --- 6. CHI TIẾT ĐƠN HÀNG ---
@login_required
@user_passes_test(is_staff)
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f"Đã cập nhật trạng thái đơn hàng #{pk} thành công!")
        return redirect('order_detail', pk=pk)

    order_items = order.items.all() 
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'order_detail.html', context)

# --- 7. BÁO CÁO DOANH THU ---
@login_required
@user_passes_test(is_staff)
def report_view(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    
    total_revenue_data = orders.filter(status='completed').aggregate(Sum('total_price'))
    total_revenue = total_revenue_data['total_price__sum'] or 0
    
    cancelled_orders = orders.filter(status='cancelled').count()
    if total_orders > 0:
        cancel_rate = round((cancelled_orders / total_orders) * 100, 1)
    else:
        cancel_rate = 0

    labels = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"]
    data = [500000, 1200000, 850000, 2000000, 1500000, 3000000, 4500000]

    top_products = [
        {'name': 'Đèn lồng đỏ', 'sold': 120, 'revenue': '18.000.000'},
        {'name': 'Bao lì xì rồng', 'sold': 95, 'revenue': '2.375.000'},
        {'name': 'Cành đào đông', 'sold': 50, 'revenue': '9.000.000'},
        {'name': 'Dây treo thần tài', 'sold': 45, 'revenue': '1.125.000'},
    ]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'cancel_rate': cancel_rate,
        'chart_labels_json': json.dumps(labels),
        'chart_data_json': json.dumps(data),
        'top_products': top_products
    }
    return render(request, 'report.html', context)