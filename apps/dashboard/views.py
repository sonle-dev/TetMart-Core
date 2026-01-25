import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required(login_url='core:login')
def dashboard_view(request):
    # Dữ liệu giả lập (Mock Data) cập nhật mới
    context = {
        'revenue': '45.200.000',      # Doanh thu (Đã đổi số mới)
        'count_new': 12,              # Số đơn mới
        'count_processing': 8,        # Số đơn chờ xử lý
        'count_shipping': 5,          # Số đơn đang giao
        'count_completed': 45,        # Số đơn hoàn thành
        'count_cancelled': 3,         # Số đơn đã hủy
        
        # Thêm biến này để bảng danh sách bên dưới không bị lỗi
        'total_orders': 150,          
        'total_products': 48          
    }
    return render(request, 'dashboard.html', context)
@login_required(login_url='core:login')
def report_view(request):
    # 1. Dữ liệu cho Biểu đồ (Doanh thu 7 ngày gần nhất)
    chart_labels = ["30/12", "31/12", "01/01", "02/01", "03/01", "04/01", "05/01"]
    chart_data = [4200000, 5100000, 6800000, 5900000, 7200000, 6500000, 8600000]

    # 2. Dữ liệu Top sản phẩm bán chạy
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
        # Chuyển dữ liệu Python sang JSON để JavaScript đọc được
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'dashboard/report.html', context)

@login_required(login_url='core:login')
def order_list_view(request):
    # Dữ liệu giả lập danh sách đơn hàng
    orders = [
        {
            'id': 'DH001', 
            'customer': 'Nguyễn Văn An', 
            'phone': '0901234567', 
            'address': '123 Nguyễn Trãi, Thanh Xuân, Hà Nội',
            'total': '1.250.000đ', 
            'status': 'pending', # Chờ xử lý
            'date': '05/01/2026'
        },
        {
            'id': 'DH002', 
            'customer': 'Trần Thị Bình', 
            'phone': '0912345678', 
            'address': '456 Láng Hạ, Đống Đa, Hà Nội',
            'total': '645.000đ', 
            'status': 'pending', 
            'date': '05/01/2026'
        },
        {
            'id': 'DH003', 
            'customer': 'Lê Văn Cường', 
            'phone': '0923456789', 
            'address': '789 Giảng Võ, Ba Đình, Hà Nội',
            'total': '580.000đ', 
            'status': 'shipping', # Đang giao
            'date': '04/01/2026'
        },
        {
            'id': 'DH004', 
            'customer': 'Phạm Thu Hà', 
            'phone': '0934567890', 
            'address': '12 Hàng Bài, Hoàn Kiếm, Hà Nội',
            'total': '2.100.000đ', 
            'status': 'completed', # Hoàn thành
            'date': '03/01/2026'
        },
    ]

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)
# 👇 Thêm hàm này vào cuối file apps/dashboard/views.py
@login_required(login_url='core:login')
def order_detail_view(request, order_id):
    # Dữ liệu giả lập cho 1 đơn hàng cụ thể
    order = {
        'id': order_id,
        'customer': 'Nguyễn Văn An',
        'phone': '0901234567',
        'address': '123 Nguyễn Trãi, Thanh Xuân, Hà Nội',
        'note': 'Giao trước 10h sáng',
        'status': 'pending', # Đang chờ xử lý
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
