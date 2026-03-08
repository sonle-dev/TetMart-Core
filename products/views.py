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
    context = {'orders': orders, 'active_page': 'orders'}
    
    return render(request, 'dashboard/orders.html', context)

# VIEW DANH SÁCH SẢN PHẨM
@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_products_view(request):
    products = Product.objects.all().order_by('-id')
    context = {'products': products, 'active_page': 'products'}
    return render(request, 'dashboard/products.html', context)

#  VIEW TRANG CHỦ 
def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'index.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
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
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    context = {
        'revenue': revenue,
        'count_new': count_new,
        'count_shipping': count_shipping,
        'count_completed': count_completed,
        'count_cancelled': count_cancelled,
        'recent_orders': recent_orders,
        'active_page': 'dashboard'
    }
 
    return render(request, 'dashboard/dashboard.html', context)
# VIEW BÁO CÁO DOANH THU
@login_required(login_url='login')
@user_passes_test(is_staff)
def report_view(request):
    # Logic tính toán 
    revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    context = {
        'revenue': revenue,
        'active_page': 'report' 
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

    

    context = {
        'order': order,
        'active_page': 'orders'
    }
<<<<<<< Updated upstream
    return render(request, 'dashboard/order_detail.html', context)
=======
    return render(request, 'dashboard/order_detail.html', context)

def product_create(request):
    return render(request, 'dashboard/product_create.html')

# products/views.py

def product_edit(request, pk):
   
    fake_product = {
        'name': 'Giỏ Quà Tết Sum Vầy 2026',
        'category': 'Quà biếu',
        'price': 500000,
        'stock': 50,
        'description': 'Sản phẩm bán chạy nhất dịp Tết, phù hợp biếu tặng.'
    }
    
    context = {
        'active_page': 'products',
        'product': fake_product  
    }
    return render(request, 'dashboard/product_edit.html', context)

def product_delete(request, pk):
   
    product = get_object_or_404(Product, pk=pk)
    
    
    product.delete()
    
    return redirect('product_list')
>>>>>>> Stashed changes
