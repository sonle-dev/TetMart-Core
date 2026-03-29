from datetime import datetime, timedelta, time
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Category
from orders.models import Order
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncDate
from django.utils import timezone
from collections import defaultdict
from orders.models import Order, OrderItem


# Hàm kiểm tra admin
def is_staff(user):
    return user.is_staff

# VIEW DANH SÁCH ĐƠN HÀNG 
@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_orders_view(request):
    orders = Order.objects.all().order_by('-created_at')

    for order in orders:
        order.formatted_total_price = f"{int(order.total_price or 0):,}".replace(",", ".")

    context = {
        'orders': orders,
        'active_page': 'orders',
    }

    return render(request, 'dashboard/orders.html', context)

# VIEW DANH SÁCH SẢN PHẨM
@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_products_view(request):
    products = Product.objects.all().order_by('-id')
    context = {'products': products, 'active_page': 'products'}
    return render(request, 'dashboard/product_list.html', context)
    

#  VIEW TRANG CHỦ 
def home(request):
    products = Product.objects.filter(is_active=True)

    daily_suggestions = Product.objects.filter(is_active=True).order_by('?')[:4]


    return render(request, 'index.html', {
        'products': products,
        'daily_suggestions': daily_suggestions
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {
        'product': product
    })

# VIEW DASHBOARD TỔNG QUAN 
@login_required(login_url='login')
def dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    recent_orders = list(orders[:5])

    total_orders = orders.count()
    total_products = Product.objects.count()

    total_revenue = (
        orders.filter(status='completed')
        .aggregate(total=Sum('total_price'))['total'] or 0
    )

    formatted_revenue = f"{int(total_revenue):,}".replace(",", ".")

    for order in recent_orders:
        order.formatted_total_price = f"{int(order.total_price or 0):,}".replace(",", ".")

    count_new = orders.filter(status='new').count()
    count_processing = orders.filter(status='pending').count()
    count_shipping = orders.filter(status='shipping').count()
    count_completed = orders.filter(status='completed').count()
    count_cancelled = orders.filter(status='cancelled').count()

    
    context = {
        'formatted_revenue': formatted_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'count_new': count_new,
        'count_processing': count_processing,
        'count_shipping': count_shipping,
        'count_completed': count_completed,
        'count_cancelled': count_cancelled,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)
# VIEW BÁO CÁO DOANH THU
@login_required(login_url='login')
def report_view(request):
    days = int(request.GET.get('days', 7))
    start_day = timezone.localdate() - timedelta(days=days - 1)
    start_dt = timezone.make_aware(datetime.combine(start_day, time.min))

    orders = Order.objects.filter(created_at__gte=start_dt)
    completed_orders = orders.filter(status='completed')
    cancelled_orders = orders.filter(status='cancelled')

    total_revenue = completed_orders.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    total_orders = completed_orders.count()
    cancelled_count = cancelled_orders.count()
    cancel_rate = round((cancelled_count / total_orders) * 100, 1) if total_orders else 0

    revenue_by_day = (
        completed_orders
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('total_price'))
        .order_by('day')
    )

    orders_by_day = (
        completed_orders
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )
    
    category_revenue = (
        OrderItem.objects
        .filter(order__status='completed', order__created_at__gte=start_dt)
        .values('product__category__name')
        .annotate(
            revenue=Sum(
                ExpressionWrapper(
                    F('price') * F('quantity'),
                    output_field=DecimalField(max_digits=12, decimal_places=0)
                )
            )
        )
        .order_by('-revenue')
    )

    top_products = (
        OrderItem.objects
        .filter(order__status='completed', order__created_at__gte=start_dt)
        .values('product__id', 'product__name')
        .annotate(
            sold=Sum('quantity'),
            revenue=Sum(
                ExpressionWrapper(
                    F('price') * F('quantity'),
                    output_field=DecimalField(max_digits=12, decimal_places=0)
                )
            )
        )
        .order_by('-sold')[:5]
    )

   
    # map doanh thu theo ngày bằng CHUỖI ngày
    revenue_map = {
        item['day'].strftime('%d/%m'): float(item['total'] or 0)
        for item in revenue_by_day if item['day']
    }

    # map số đơn theo ngày bằng CHUỖI ngày
    order_map = {
        item['day'].strftime('%d/%m'): item['total']
        for item in orders_by_day if item['day']
    }

    # tạo đủ danh sách ngày theo bộ lọc
    all_day_objs = [start_day + timedelta(days=i) for i in range(days)]
    all_days = [day.strftime('%d/%m') for day in all_day_objs]

    # gom doanh thu và số đơn theo ngày bằng Python
    revenue_map = defaultdict(float)
    order_map = defaultdict(int)

    for order in completed_orders:
        order_day = timezone.localtime(order.created_at).date().strftime('%d/%m')
        revenue_map[order_day] += float(order.total_price or 0)
        order_map[order_day] += 1

    chart_labels = all_days
    chart_data = [revenue_map.get(day, 0) for day in all_days]

    order_chart_labels = all_days
    order_chart_data = [order_map.get(day, 0) for day in all_days]

    category_labels = [item['product__category__name'] or 'Khác' for item in category_revenue]
    category_data = [float(item['revenue']) for item in category_revenue]

    formatted_top_products = []
    for item in top_products:
        formatted_top_products.append({
            'name': item['product__name'],
            'sold': item['sold'],
            'revenue': f"{int(item['revenue'] or 0):,}".replace(",", "."),
        })
    
    context = {
        'total_revenue': f"{int(total_revenue):,}".replace(",", "."),
        'total_orders': total_orders,
        'cancel_rate': cancel_rate,
        'top_products': formatted_top_products,

        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),

        'order_chart_labels_json': json.dumps(order_chart_labels),
        'order_chart_data_json': json.dumps(order_chart_data),

        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),

        'active_page': 'report',
        'days': days,
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
        'active_page': 'orders'
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
    
@login_required
def dashboard_products_view(request):
    products = Product.objects.all()
    return render(request, 'dashboard/products.html', {
        'products': products,
        'active_page': 'products'
    })
