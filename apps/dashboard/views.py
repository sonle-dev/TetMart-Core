import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# =========================================================
# 1. NHÓM DASHBOARD & BÁO CÁO
# =========================================================

@login_required(login_url='core:login')
def dashboard_view(request):
    """Trang chủ Dashboard - Tổng quan"""
    context = {
        'revenue': '45.200.000',
        'count_new': 12,
        'count_processing': 8,
        'count_shipping': 5,
        'count_completed': 45,
        'count_cancelled': 3,
        'total_orders': 150,
        'total_products': 48
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='core:login')
def report_view(request):
    """Trang Báo cáo doanh thu & Biểu đồ"""

    # 1. Dữ liệu biểu đồ doanh thu 7 ngày gần nhất
    chart_labels = ["30/12", "31/12", "01/01", "02/01", "03/01", "04/01", "05/01"]
    chart_data = [4200000, 5100000, 6800000, 5900000, 7200000, 6500000, 8600000]

    # 2. Biểu đồ mới: Số đơn hàng theo ngày
    order_chart_data = [12, 15, 19, 17, 23, 21, 27]

    # 3. Biểu đồ mới: Doanh thu theo danh mục
    category_labels = ["Bánh kẹo Tết", "Mứt Tết", "Rượu bia", "Hộp quà Tết"]
    category_data = [3250000, 1840000, 5120000, 2790000]

    # 4. Top sản phẩm bán chạy
    top_products = [
        {'id': 1, 'name': 'Bánh quy bơ Danisa 454g', 'sold': 45, 'revenue': '6.525.000'},
        {'id': 2, 'name': 'Rượu vang đỏ Chile 750ml', 'sold': 38, 'revenue': '17.100.000'},
        {'id': 3, 'name': 'Hộp bánh ABC Luxury 600g', 'sold': 32, 'revenue': '5.760.000'},
        {'id': 4, 'name': 'Hạt điều rang muối 500g', 'sold': 28, 'revenue': '6.160.000'},
        {'id': 5, 'name': 'Bia Heineken lon 330ml', 'sold': 25, 'revenue': '1.625.000'},
    ]

    context = {
        'total_revenue': '1.230.000',
        'total_orders': 7,
        'cancel_rate': '14.3',
        'top_products': top_products,

        # Biểu đồ cũ
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),

        # Biểu đồ mới 1: số đơn hàng
        'order_chart_data_json': json.dumps(order_chart_data),

        # Biểu đồ mới 2: doanh thu theo danh mục
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),
    }
    return render(request, 'dashboard/report.html', context)


# =========================================================
# 2. NHÓM QUẢN LÝ ĐƠN HÀNG (ORDERS)
# =========================================================

@login_required(login_url='core:login')
def order_list_view(request):
    """Danh sách tất cả đơn hàng"""
    orders = [
        {'id': 'DH001', 'customer': 'Nguyễn Văn An', 'phone': '0901234567', 'address': '123 Nguyễn Trãi, HN', 'total': '1.250.000đ', 'status': 'pending', 'date': '05/01/2026'},
        {'id': 'DH002', 'customer': 'Trần Thị Bình', 'phone': '0912345678', 'address': '456 Láng Hạ, HN', 'total': '645.000đ', 'status': 'pending', 'date': '05/01/2026'},
        {'id': 'DH003', 'customer': 'Lê Văn Cường', 'phone': '0923456789', 'address': '789 Giảng Võ, HN', 'total': '580.000đ', 'status': 'shipping', 'date': '04/01/2026'},
        {'id': 'DH004', 'customer': 'Phạm Thu Hà', 'phone': '0934567890', 'address': '12 Hàng Bài, HN', 'total': '2.100.000đ', 'status': 'completed', 'date': '03/01/2026'},
    ]
    return render(request, 'dashboard/orders.html', {'orders': orders})


@login_required(login_url='core:login')
def order_detail_view(request, order_id):
    """Chi tiết một đơn hàng cụ thể"""
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
    return render(request, 'dashboard/order_detail.html', {'order': order})


# =========================================================
# 3. NHÓM QUẢN LÝ SẢN PHẨM (PRODUCTS)
# =========================================================

@login_required(login_url='core:login')
def product_list_view(request):
    """Danh sách sản phẩm"""
    products = [
        {'id': 1, 'code': 'P001', 'name': 'Bánh quy bơ Danisa 454g', 'category': 'Bánh kẹo Tết', 'price': '145.000đ', 'stock': 50, 'status': 'active'},
        {'id': 2, 'code': 'P002', 'name': 'Hộp bánh ABC Luxury 600g', 'category': 'Bánh kẹo Tết', 'price': '180.000đ', 'stock': 30, 'status': 'active'},
        {'id': 3, 'code': 'P003', 'name': 'Mứt gừng Hưng Yên 500g', 'category': 'Mứt Tết', 'price': '95.000đ', 'stock': 0, 'status': 'inactive'},
        {'id': 4, 'code': 'P004', 'name': 'Rượu vang đỏ Chile 750ml', 'category': 'Rượu bia', 'price': '450.000đ', 'stock': 12, 'status': 'active'},
    ]
    return render(request, 'dashboard/products.html', {'products': products})


@login_required(login_url='core:login')
def product_edit_view(request, product_id):
    """Form chỉnh sửa sản phẩm"""
    product = {
        'id': product_id,
        'code': 'P001',
        'name': 'Bánh quy bơ Danisa 454g',
        'category': 'Bánh kẹo Tết',
        'price': '145000',
        'stock': 50,
        'description': 'Bánh quy bơ nhập khẩu...',
        'image': 'product.jpg'
    }
    return render(request, 'dashboard/product_edit.html', {'product': product})


@login_required(login_url='core:login')
def product_delete_view(request, product_id):
    """Xử lý xóa sản phẩm"""
    # Logic xóa DB sẽ nằm ở đây: Product.objects.get(id=product_id).delete()
    return redirect('core:products')


@login_required(login_url='core:login')
def product_create_view(request):
    """Trang thêm sản phẩm mới"""
    # Logic xử lý lưu dữ liệu (POST) sẽ viết sau
    # Hiện tại chỉ hiển thị form trống
    return render(request, 'dashboard/product_create.html')