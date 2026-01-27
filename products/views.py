from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product
from orders.models import Order
from django.db.models import Sum

# Hàm kiểm tra admin
def is_staff(user):
    return user.is_staff

# VIEW DANH SÁCH ĐƠN HÀNG 
@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_orders_view(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {'orders': orders, 'active_tab': 'orders'}
    
    return render(request, 'dashboard/orders.html', context)

# VIEW DANH SÁCH SẢN PHẨM
@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_products_view(request):
    products = Product.objects.all().order_by('-id')
    context = {'products': products, 'active_tab': 'products'}
    return render(request, 'dashboard/product_list.html', context)

#  VIEW TRANG CHỦ 
def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# VIEW DASHBOARD TỔNG QUAN 
@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_view(request):
    # Tính toán số liệu
    revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    count_new = Order.objects.filter(status='pending').count()
    count_shipping = Order.objects.filter(status='shipping').count()
    count_completed = Order.objects.filter(status='completed').count()
    count_cancelled = Order.objects.filter(status='cancelled').count()
    
    # Lấy 5 đơn mới nhất
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'revenue': revenue,
        'count_new': count_new,
        'count_shipping': count_shipping,
        'count_completed': count_completed,
        'count_cancelled': count_cancelled,
        'recent_orders': recent_orders,
        'active_tab': 'dashboard'
    }
 
    return render(request, 'dashboard.html', context)
# VIEW BÁO CÁO DOANH THU
@login_required(login_url='login')
@user_passes_test(is_staff)
def report_view(request):
    # Logic tính toán 
    revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    context = {
        'revenue': revenue,
        'active_tab': 'report' 
    }
    return render(request, 'dashboard/report.html', context)

#  VIEW CHI TIẾT ĐƠN HÀNG 
@login_required(login_url='login')
@user_passes_test(is_staff)
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return redirect('order_detail', pk=pk)

    try:
        order_items = order.items.all()
    except:
        from orders.models import OrderItem
        order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
        'active_tab': 'orders'
    }
    return render(request, 'dashboard/order_detail.html', context)