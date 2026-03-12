import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.db.models import Sum
from orders.models import Order

@login_required(login_url='core:login')
def dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    recent_orders = orders[:5]

    total_orders = orders.count()
    total_products = Product.objects.count()

    total_revenue = (
        orders.filter(status='completed')
        .aggregate(total=Sum('total_price'))['total'] or 0
    )

    count_new = orders.filter(status='pending').count()
    count_processing = orders.filter(status='processing').count()
    count_shipping = orders.filter(status='shipping').count()
    count_completed = orders.filter(status='completed').count()
    count_cancelled = orders.filter(status='cancelled').count()

    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'revenue': total_revenue,

        'count_new': count_new,
        'count_processing': count_processing,
        'count_shipping': count_shipping,
        'count_completed': count_completed,
        'count_cancelled': count_cancelled,

        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard/dashboard.html', context)
@login_required(login_url='core:login')
def report_view(request):
    #  Dữ liệu cho Biểu đồ 
    chart_labels = ["30/12", "31/12", "01/01", "02/01", "03/01", "04/01", "05/01"]
    chart_data = [4200000, 5100000, 6800000, 5900000, 7200000, 6500000, 8600000]

    #  Dữ liệu Top sản phẩm bán chạy
    top_products = [
        {'id': 1, 'name': 'Bánh quy bơ Danisa 454g', 'sold': 45, 'revenue': '6.525.000'},
        {'id': 2, 'name': 'Rượu vang đỏ Chile 750ml', 'sold': 38, 'revenue': '17.100.000'},
        {'id': 3, 'name': 'Hộp bánh ABC Luxury 600g', 'sold': 32, 'revenue': '5.760.000'},
        {'id': 4, 'name': 'Hạt điều rang muối 500g', 'sold': 28, 'revenue': '6.160.000'},
        {'id': 5, 'name': 'Bia Heineken lon 330ml (lốc 6)', 'sold': 25, 'revenue': '1.625.000'},
    ]

    context = {
        'total_revenue': '1.230.000',
        'total_orders': 7,
        'cancel_rate': '14.3',
        'top_products': top_products,
        # Chuyển dữ liệu 
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'dashboard/report.html', context)

@login_required(login_url='core:login')
def order_list_view(request):
    orders = Order.objects.select_related('user').all().order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)

@login_required(login_url='core:login')
def order_detail_view(request, order_id):
    # Dữ liệu giả lập 
    order = {
        'id': order_id,
        'customer': 'Nguyễn Văn An',
        'phone': '0901234567',
        'address': '123 Nguyễn Trãi, Thanh Xuân, Hà Nội',
        'note': 'Giao trước 10h sáng',
        'status': 'pending', 
        'created_at': '05/01/2026',
        'items': [
            {'name': 'Bánh quy bơ Danisa 454g', 'quantity': 2, 'price': '145.000đ', 'total': '290.000đ'},
            {'name': 'Rượu vang đỏ Chile 750ml', 'quantity': 2, 'price': '450.000đ', 'total': '900.000đ'},
            {'name': 'Hạt điều rang muối 500g', 'quantity': 1, 'price': '220.000đ', 'total': '220.000đ'},
        ],
        'total_money': '1.410.000đ'
    }
    
    context = {
        'order': order
    }
    return render(request, 'dashboard/order_detail.html', context)
def product_list_view(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "dashboard/products.html", {"products": products})

def product_create_view(request):
    # tạm thời render trang form (nếu bạn đã có form thì xử lý POST sau)
    return render(request, "dashboard/product_create.html")

def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "dashboard/product_edit.html", {"product": product})

def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("core:product_list")

