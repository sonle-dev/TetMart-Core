from datetime import datetime, timedelta, time
import json
<<<<<<< HEAD

=======
from django.contrib import messages
>>>>>>> develop
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product, Category
from orders.models import Order
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncDate
from django.utils import timezone
from collections import defaultdict
from orders.models import Order, OrderItem
<<<<<<< HEAD

=======
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
>>>>>>> develop

from tetmart.permission_utils import (
    DASHBOARD_PERMS,
    ORDER_PERMS,
    CUSTOMER_PERMS,
    PRODUCT_PERMS,
    REPORT_PERMS,
    has_any_perm,
    first_allowed_dashboard_name,
    permission_gate,
)


def has_dashboard_permission(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm('auth.view_dashboard')
        or user.has_perm('auth.view_revenue_dashboard')
    )


def has_order_permission(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm('orders.view_order')
        or user.has_perm('orders.update_order_status')
        or user.has_perm('orders.export_order')
        or user.has_perm('orders.cancel_order')
    )


def has_product_permission(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm('products.view_product')
        or user.has_perm('products.add_product')
        or user.has_perm('products.change_product')
        or user.has_perm('products.delete_product')
        or user.has_perm('products.hide_product')
    )


def has_customer_permission(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm('users.view_customer_list')
        or user.has_perm('users.view_customer_detail')
        or user.has_perm('users.create_customer')
        or user.has_perm('users.lock_customer')
    )


def has_report_permission(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm('auth.view_report')
        or user.has_perm('auth.export_report')
        or user.has_perm('auth.view_revenue_report')
    )
# VIEW DANH SÁCH ĐƠN HÀNG 
@permission_gate('orders.view_order')
def dashboard_orders_view(request):
<<<<<<< HEAD
    orders = Order.objects.all().order_by('-created_at')

    for order in orders:
        order.formatted_total_price = f"{int(order.total_price or 0):,}".replace(",", ".")

    context = {
        'orders': orders,
        'active_page': 'orders',
=======
    orders = Order.objects.select_related('user').all()

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')
    sort = request.GET.get('sort', 'newest')

    if q:
        order_id = q.replace('#DH', '').replace('DH', '').strip()
        query = (
            Q(user__username__icontains=q) |
            Q(full_name__icontains=q) |
            Q(phone__icontains=q)
        )

        if order_id.isdigit():
            query |= Q(id=int(order_id))

        orders = orders.filter(query)

    if status and status != 'all':
        orders = orders.filter(status=status)

    if sort == 'oldest':
        orders = orders.order_by('created_at')
    else:
        orders = orders.order_by('-created_at')

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for order in page_obj:
        order.formatted_total_price = f"{int(order.total_price or 0):,}".replace(",", ".")

    context = {
        'orders': page_obj,
        'page_obj': page_obj,
        'active_page': 'orders',
        'filters': {
            'q': q,
            'status': status,
            'sort': sort,
        }
>>>>>>> develop
    }

    return render(request, 'dashboard/orders.html', context)

# VIEW DANH SÁCH SẢN PHẨM
@login_required(login_url='login')
@user_passes_test(has_product_permission, login_url='home')
@permission_gate('products.view_product')
def dashboard_products_view(request):
<<<<<<< HEAD
    products = Product.objects.all().order_by('-id')
    context = {'products': products, 'active_page': 'products'}
    return render(request, 'dashboard/product_list.html', context)
=======
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all().order_by('name')

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all')
    status = request.GET.get('status', 'all')
    sort = request.GET.get('sort', 'newest')

    if q:
        product_id = q.replace('#SP', '').replace('SP', '').strip()
        query = Q(name__icontains=q) | Q(slug__icontains=q)

        if product_id.isdigit():
            query |= Q(id=int(product_id))

        products = products.filter(query)

    if category != 'all' and str(category).isdigit():
        products = products.filter(category_id=int(category))

    if status == 'in_stock':
        products = products.filter(is_active=True, stock__gt=0)
    elif status == 'out_stock':
        products = products.filter(Q(is_active=False) | Q(stock__lte=0))

    if sort == 'oldest':
        products = products.order_by('id')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-id')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'active_page': 'products',
        'filters': {
            'q': q,
            'category': category,
            'status': status,
            'sort': sort,
        }
    }

    return render(request, 'dashboard/products.html', context)
>>>>>>> develop
    

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
<<<<<<< HEAD
def dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    recent_orders = list(orders[:5])
=======
@user_passes_test(has_dashboard_permission, login_url='home')
def dashboard_view(request):
    if not has_any_perm(request.user, DASHBOARD_PERMS):
        target = first_allowed_dashboard_name(request.user)
        if target and target != 'dashboard':
            return redirect(target)

        messages.error(request, 'Bạn không có quyền truy cập trang quản trị.')
        return redirect('home')

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
>>>>>>> develop

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
<<<<<<< HEAD
=======
        'active_page': 'dashboard',
>>>>>>> develop
    }
    return render(request, 'dashboard/dashboard.html', context)
@permission_gate(*CUSTOMER_PERMS)
def dashboard_customers(request):
    User = get_user_model()

    customers_qs = User.objects.filter(is_customer=True).annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total_price')
    )

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')
    sort = request.GET.get('sort', 'newest')

    if q:
        code_number = q.replace('KH', '').strip()
        query = (
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q)
        )

        if code_number.isdigit():
            query |= Q(id=int(code_number))

        customers_qs = customers_qs.filter(query)

    if sort == 'name_asc':
        customers_qs = customers_qs.order_by('username')
    elif sort == 'orders_desc':
        customers_qs = customers_qs.order_by('-order_count')
    elif sort == 'spent_desc':
        customers_qs = customers_qs.order_by('-total_spent')
    else:
        customers_qs = customers_qs.order_by('-date_joined')

    customer_list = []
    for user in customers_qs:
        order_count = user.order_count or 0
        total_spent = user.total_spent or 0

        if not user.is_active:
            customer_status = 'inactive'
        elif total_spent >= 500000:
            customer_status = 'vip'
        elif order_count > 0:
            customer_status = 'active'
        else:
            customer_status = 'new'

        if status != 'all' and customer_status != status:
            continue

        customer_list.append({
            'id': user.id,
            'avatar': (user.username[:1] or 'K').upper(),
            'name': user.get_full_name() or user.username,
            'email': user.email or 'Chưa cập nhật',
            'phone': user.phone or 'Chưa cập nhật',
            'city': user.address or 'Chưa cập nhật',
            'code': f'KH{user.id:03d}',
            'order_count': order_count,
            'total_spent_display': f"{int(total_spent):,}đ".replace(",", "."),
            'status': customer_status,
            'joined_at': user.date_joined.strftime('%d/%m/%Y'),
        })

    customer_stats = {
        'all': User.objects.filter(is_customer=True).count(),
        'new': sum(1 for c in customer_list if c['status'] == 'new'),
        'active': sum(1 for c in customer_list if c['status'] == 'active'),
        'vip': sum(1 for c in customer_list if c['status'] == 'vip'),
    }

    context = {
        'active_page': 'customers',
        'customers': customer_list,
        'customer_stats': customer_stats,
        'filters': {
            'q': q,
            'status': status,
            'sort': sort,
        },
    }

    return render(request, 'dashboard/customers.html', context)
# VIEW BÁO CÁO DOANH THU
<<<<<<< HEAD
@login_required(login_url='login')
=======
@permission_gate(*REPORT_PERMS)
>>>>>>> develop
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
<<<<<<< HEAD
#  VIEW CHI TIẾT ĐƠN HÀNG 
@login_required(login_url='login')
@user_passes_test(is_staff)
=======
# VIEW CHI TIẾT ĐƠN HÀNG
@permission_gate('orders.view_order')
>>>>>>> develop
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        if not request.user.is_superuser and not request.user.has_perm('orders.update_order_status'):
            messages.error(request, 'Bạn không có quyền cập nhật trạng thái đơn hàng.')
            return redirect('order_detail', pk=pk)

        new_status = request.POST.get('status')
        allowed_status = ['new', 'pending', 'shipping', 'completed', 'cancelled']

        if new_status in allowed_status:
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
<<<<<<< HEAD
        'active_page': 'orders'
    }

    

    context = {
        'order': order,
=======
>>>>>>> develop
        'active_page': 'orders'
    }

    return render(request, 'dashboard/order_detail.html', context)

@login_required(login_url='login')
@user_passes_test(has_product_permission, login_url='home')
@permission_gate('products.add_product')
def product_create(request):
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category')
        price = request.POST.get('price') or 0
        stock = request.POST.get('stock') or 0
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('images')

        form_data = {
            'name': name,
            'category': category_id,
            'price': price,
            'stock': stock,
            'description': description,
        }

        if not name or not category_id or int(price) <= 0 or int(stock) < 0:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin hợp lệ.')
            return render(request, 'dashboard/product_create.html', {
                'active_page': 'products',
                'categories': categories,
                'form_data': form_data,
            })

        product = Product.objects.create(
            name=name,
            category_id=category_id,
            price=price,
            stock=stock,
            description=description,
            image=image,
            is_active=True,
        )

        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product.slug = slug
        product.save()

        messages.success(request, 'Thêm sản phẩm thành công.')
        return redirect('dashboard_products')

    return render(request, 'dashboard/product_create.html', {
        'active_page': 'products',
        'categories': categories,
        'form_data': {},
    })

# products/views.py
@login_required(login_url='login')
@user_passes_test(has_product_permission, login_url='home')
@permission_gate('products.change_product')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        product.name = request.POST.get('name', '').strip()
        product.category_id = request.POST.get('category')
        product.price = request.POST.get('price') or 0
        product.stock = request.POST.get('stock') or 0
        product.description = request.POST.get('description', '').strip()

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product.slug = slug

        product.save()
        messages.success(request, 'Cập nhật sản phẩm thành công.')
        return redirect('dashboard_products')

    context = {
        'active_page': 'products',
        'product': product,
        'categories': categories,
    }
    return render(request, 'dashboard/product_edit.html', context)

@login_required(login_url='login')
@user_passes_test(has_product_permission, login_url='home')
@permission_gate('products.delete_product')
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
<<<<<<< HEAD
    
@login_required
def dashboard_products_view(request):
    products = Product.objects.all()
    return render(request, 'dashboard/products.html', {
        'products': products,
        'active_page': 'products'
    })
=======

>>>>>>> develop
