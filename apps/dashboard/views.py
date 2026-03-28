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

    chart_labels = ["30/12", "31/12", "01/01", "02/01", "03/01", "04/01", "05/01"]
    chart_data = [4200000, 5100000, 6800000, 5900000, 7200000, 6500000, 8600000]

    order_chart_data = [12, 15, 19, 17, 23, 21, 27]

    category_labels = ["Bánh kẹo Tết", "Mứt Tết", "Rượu bia", "Hộp quà Tết"]
    category_data = [3250000, 1840000, 5120000, 2790000]

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
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
        'order_chart_data_json': json.dumps(order_chart_data),
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
    return redirect('core:products')


@login_required(login_url='core:login')
def product_create_view(request):
    """Trang thêm sản phẩm mới"""
    return render(request, 'dashboard/product_create.html')


# =========================================================
# 4. NHÓM QUẢN LÝ KHÁCH HÀNG (CUSTOMERS)
# =========================================================

def lay_danh_sach_khach_hang_mau():
    danh_sach_khach_hang = [
        {
            'id': 1,
            'ma_khach_hang': 'KH001',
            'ho_ten': 'Nguyễn Văn An',
            'so_dien_thoai': '0901234567',
            'email': 'an.nguyen@gmail.com',
            'tinh_thanh': 'Hà Nội',
            'dia_chi': '123 Nguyễn Trãi, Thanh Xuân, Hà Nội',
            'so_don_hang': 1,
            'tong_chi_tieu_hien_thi': '250.000đ',
            'tong_chi_tieu': 250000,
            'trang_thai': 'khach_moi',
            'ngay_tham_gia_hien_thi': '05/01/2026',
            'ngay_tham_gia_sap_xep': '2026-01-05',
            'ghi_chu': 'Khách mới đăng ký đầu tháng 1.',
        },
        {
            'id': 2,
            'ma_khach_hang': 'KH002',
            'ho_ten': 'Trần Thị Bình',
            'so_dien_thoai': '0912345678',
            'email': 'binh.tran@gmail.com',
            'tinh_thanh': 'Đà Nẵng',
            'dia_chi': '45 Nguyễn Văn Linh, Hải Châu, Đà Nẵng',
            'so_don_hang': 8,
            'tong_chi_tieu_hien_thi': '2.180.000đ',
            'tong_chi_tieu': 2180000,
            'trang_thai': 'than_thiet',
            'ngay_tham_gia_hien_thi': '08/01/2026',
            'ngay_tham_gia_sap_xep': '2026-01-08',
            'ghi_chu': 'Khách hàng mua lặp lại nhiều lần.',
        },
        {
            'id': 3,
            'ma_khach_hang': 'KH003',
            'ho_ten': 'Lê Văn Cường',
            'so_dien_thoai': '0923456789',
            'email': 'cuong.le@gmail.com',
            'tinh_thanh': 'Hải Phòng',
            'dia_chi': '78 Lạch Tray, Ngô Quyền, Hải Phòng',
            'so_don_hang': 3,
            'tong_chi_tieu_hien_thi': '690.000đ',
            'tong_chi_tieu': 690000,
            'trang_thai': 'ngung_hoat_dong',
            'ngay_tham_gia_hien_thi': '11/01/2026',
            'ngay_tham_gia_sap_xep': '2026-01-11',
            'ghi_chu': 'Đã lâu chưa quay lại mua hàng.',
        },
        {
            'id': 4,
            'ma_khach_hang': 'KH004',
            'ho_ten': 'Phạm Thu Hà',
            'so_dien_thoai': '0934567890',
            'email': 'ha.pham@gmail.com',
            'tinh_thanh': 'TP. Hồ Chí Minh',
            'dia_chi': '12 Điện Biên Phủ, Bình Thạnh, TP. Hồ Chí Minh',
            'so_don_hang': 15,
            'tong_chi_tieu_hien_thi': '5.960.000đ',
            'tong_chi_tieu': 5960000,
            'trang_thai': 'vip',
            'ngay_tham_gia_hien_thi': '15/01/2026',
            'ngay_tham_gia_sap_xep': '2026-01-15',
            'ghi_chu': 'Khách VIP, ưu tiên chăm sóc.',
        },
        {
            'id': 5,
            'ma_khach_hang': 'KH005',
            'ho_ten': 'Vũ Minh Đức',
            'so_dien_thoai': '0945678901',
            'email': 'duc.vu@gmail.com',
            'tinh_thanh': 'Bắc Ninh',
            'dia_chi': '90 Lý Thái Tổ, Bắc Ninh',
            'so_don_hang': 6,
            'tong_chi_tieu_hien_thi': '1.240.000đ',
            'tong_chi_tieu': 1240000,
            'trang_thai': 'than_thiet',
            'ngay_tham_gia_hien_thi': '17/01/2026',
            'ngay_tham_gia_sap_xep': '2026-01-17',
            'ghi_chu': 'Thường mua quà Tết cho doanh nghiệp.',
        },
        {
            'id': 6,
            'ma_khach_hang': 'KH006',
            'ho_ten': 'Đặng Hải Yến',
            'so_dien_thoai': '0956789012',
            'email': 'yen.dang@gmail.com',
            'tinh_thanh': 'Thái Nguyên',
            'dia_chi': 'Khu đô thị Yên Bình, Phổ Yên, Thái Nguyên',
            'so_don_hang': 1,
            'tong_chi_tieu_hien_thi': '420.000đ',
            'tong_chi_tieu': 420000,
            'trang_thai': 'khach_moi',
            'ngay_tham_gia_hien_thi': '19/01/2026',
            'ngay_tham_gia_sap_xep': '2026-01-19',
            'ghi_chu': 'Mới mua đơn đầu tiên.',
        },
    ]

    for khach_hang in danh_sach_khach_hang:
        khach_hang['ky_tu_dai_dien'] = khach_hang['ho_ten'].split()[-1][0].upper()

    return danh_sach_khach_hang


@login_required(login_url='core:login')
def customer_list_view(request):
    """Danh sách khách hàng"""
    danh_sach_khach_hang = lay_danh_sach_khach_hang_mau()

    tu_khoa = (request.GET.get('q') or '').strip().lower()
    trang_thai = (request.GET.get('status') or 'tat_ca').strip()
    sap_xep = (request.GET.get('sort') or 'moi_nhat').strip()

    ket_qua = list(danh_sach_khach_hang)

    if tu_khoa:
        ket_qua = [
            kh for kh in ket_qua
            if tu_khoa in kh['ho_ten'].lower()
            or tu_khoa in kh['ma_khach_hang'].lower()
            or tu_khoa in kh['so_dien_thoai'].lower()
            or tu_khoa in kh['email'].lower()
        ]

    if trang_thai != 'tat_ca':
        ket_qua = [kh for kh in ket_qua if kh['trang_thai'] == trang_thai]

    if sap_xep == 'ten_a_z':
        ket_qua.sort(key=lambda kh: kh['ho_ten'])
    elif sap_xep == 'nhieu_don_nhat':
        ket_qua.sort(key=lambda kh: kh['so_don_hang'], reverse=True)
    elif sap_xep == 'chi_tieu_cao_nhat':
        ket_qua.sort(key=lambda kh: kh['tong_chi_tieu'], reverse=True)
    elif sap_xep == 'cu_nhat':
        ket_qua.sort(key=lambda kh: kh['ngay_tham_gia_sap_xep'])
    else:
        ket_qua.sort(key=lambda kh: kh['ngay_tham_gia_sap_xep'], reverse=True)

    context = {
        'danh_sach_khach_hang': ket_qua,
        'bo_loc': {
            'q': request.GET.get('q', ''),
            'status': trang_thai,
            'sort': sap_xep,
        },
        'tong_khach_hang': len(danh_sach_khach_hang),
        'khach_moi': sum(1 for kh in danh_sach_khach_hang if kh['trang_thai'] == 'khach_moi'),
        'khach_hang_than_thiet': sum(1 for kh in danh_sach_khach_hang if kh['trang_thai'] == 'than_thiet'),
        'khach_vip': sum(1 for kh in danh_sach_khach_hang if kh['trang_thai'] == 'vip'),
        'khach_ngung_hoat_dong': sum(1 for kh in danh_sach_khach_hang if kh['trang_thai'] == 'ngung_hoat_dong'),
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='core:login')
def customer_create_view(request):
    """Trang thêm khách hàng"""
    return render(request, 'dashboard/customer_create.html')


@login_required(login_url='core:login')
def customer_detail_view(request, customer_id):
    """Trang chi tiết khách hàng"""
    danh_sach_khach_hang = lay_danh_sach_khach_hang_mau()
    khach_hang = next((kh for kh in danh_sach_khach_hang if kh['id'] == customer_id), None)

    if not khach_hang:
        return redirect('core:customers')

    don_hang_gan_day = [
        {'ma_don': 'DH101', 'ngay_dat': '21/01/2026', 'tong_tien': '250.000đ', 'trang_thai': 'Hoàn thành'},
        {'ma_don': 'DH082', 'ngay_dat': '18/01/2026', 'tong_tien': '420.000đ', 'trang_thai': 'Đang giao'},
        {'ma_don': 'DH063', 'ngay_dat': '15/01/2026', 'tong_tien': '180.000đ', 'trang_thai': 'Chờ xử lý'},
    ]

    return render(
        request,
        'dashboard/customer_detail.html',
        {
            'khach_hang': khach_hang,
            'don_hang_gan_day': don_hang_gan_day,
        }
    )


@login_required(login_url='core:login')
def customer_lock_view(request, customer_id):
    """Trang tạm khóa khách hàng"""
    danh_sach_khach_hang = lay_danh_sach_khach_hang_mau()
    khach_hang = next((kh for kh in danh_sach_khach_hang if kh['id'] == customer_id), None)

    if not khach_hang:
        return redirect('core:customers')

    if request.method == 'POST':
        return redirect('core:customers')

    return render(
        request,
        'dashboard/customer_lock.html',
        {'khach_hang': khach_hang}
    )
@login_required(login_url='core:login')
def permission_list_view(request):
    """Trang phân quyền - frontend demo"""
    return render(request, 'dashboard/permissions.html')