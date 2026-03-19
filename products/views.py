import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.db.models import Sum, Count, F
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDate

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
    context = {'products': products, 'active_tab': 'products'}
    return render(request, 'dashboard/products.html', context)
    

#  VIEW TRANG CHỦ 
def home(request):
    products = Product.objects.filter(is_active=True)
    daily_suggestions = products[:4]

    return render(request, 'index.html', {
        'products': products,
        'daily_suggestions': daily_suggestions,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {
        'product': product
    })

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
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
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
 
 
    return render(request, 'dashboard/dashboard.html', context)
# VIEW BÁO CÁO DOANH THU
@login_required(login_url='login')
@user_passes_test(is_staff)
def report_view(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=6)

    # ===== Dữ liệu tổng quan toàn hệ thống =====
    all_orders = Order.objects.all()
    completed_orders = all_orders.filter(status='completed')
    cancelled_orders = all_orders.filter(status='cancelled')

    total_revenue = completed_orders.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    total_orders = all_orders.count()
    cancelled_count = cancelled_orders.count()
    cancel_rate = round((cancelled_count / total_orders) * 100, 1) if total_orders > 0 else 0

        # ===== Biểu đồ theo ngày (gom bằng Python, ổn định hơn TruncDate) =====
    from collections import defaultdict

    order_count_map = defaultdict(int)
    revenue_map = defaultdict(float)

    for order in Order.objects.exclude(created_at__isnull=True):
        day = order.created_at.date()
        order_count_map[day] += 1

    for order in Order.objects.filter(status='completed').exclude(created_at__isnull=True):
        day = order.created_at.date()
        revenue_map[day] += float(order.total_price or 0)

    all_days = sorted(set(list(order_count_map.keys()) + list(revenue_map.keys())))
    all_days = all_days[-7:]

    labels = [day.strftime('%d/%m') for day in all_days]
    order_data = [order_count_map.get(day, 0) for day in all_days]
    revenue_data = [revenue_map.get(day, 0) for day in all_days]

    if not labels:
        labels = ['Không có dữ liệu']
        order_data = [0]
        revenue_data = [0]

    print("all_days =", all_days)
    print("labels =", labels)
    print("order_data =", order_data)
    print("revenue_data =", revenue_data)
    # ===== Top sản phẩm bán chạy (toàn bộ đơn completed) =====
    top_products_qs = (
        OrderItem.objects
        .filter(order__status='completed')
        .values('product__name')
        .annotate(
            sold=Sum('quantity'),
            revenue=Sum(F('quantity') * F('price'))
        )
        .order_by('-sold')[:5]
    )

    top_products = [
        {
            'name': item['product__name'],
            'sold': item['sold'] or 0,
            'revenue': item['revenue'] or 0,
        }
        for item in top_products_qs
    ]

    # ===== Tỉ trọng doanh thu theo danh mục (toàn bộ đơn completed) =====
    category_qs = (
        OrderItem.objects
        .filter(order__status='completed')
        .values('product__category__name')
        .annotate(
            revenue=Sum(F('quantity') * F('price'))
        )
        .order_by('-revenue')
    )

    category_labels = []
    category_data = []

    for item in category_qs:
        category_labels.append(item['product__category__name'] or 'Chưa phân loại')
        category_data.append(float(item['revenue'] or 0))

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'cancel_rate': cancel_rate,
        'top_products': top_products,

        'chart_labels_json': json.dumps(labels),
        'chart_data_json': json.dumps(revenue_data),
        'order_chart_data_json': json.dumps(order_data),
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),

        'active_page': 'report',
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

    

    context = {
        'order': order,
        'active_page': 'orders'
    }

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
def product_list_view(request):
    products = Product.objects.filter(is_active=True)

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all')
    price_min = request.GET.get('price_min', '').strip()
    price_max = request.GET.get('price_max', '').strip()
    sort = request.GET.get('sort', 'newest')

    if q:
        products = products.filter(name__icontains=q)

    if category and category != 'all':
        products = products.filter(category__name=category)

    if price_min:
        products = products.filter(price__gte=price_min)

    if price_max:
        products = products.filter(price__lte=price_max)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-id')

    categories = Category.objects.values_list('name', flat=True)

    context = {
        'products': products,
        'categories': categories,
        'filters': {
            'q': q,
            'category': category,
            'price_min': price_min,
            'price_max': price_max,
            'sort': sort,
        }
    }
    return render(request, 'product_list.html', context)
    
