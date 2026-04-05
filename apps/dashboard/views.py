import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from products.models import Product
from orders.models import Order
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required(login_url='login')
def dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    recent_orders = list(orders[:5])

    completed_orders = Order.objects.filter(status='completed')

    total_orders = completed_orders.count()
    total_products = Product.objects.count()

    total_revenue = (
        completed_orders.aggregate(total=Sum('total_price'))['total'] or 0
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

@login_required(login_url='login')
def dashboard_customers(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'tat_ca')
    sort = request.GET.get('sort', 'moi_nhat')

    users = User.objects.all().order_by('-date_joined')

    danh_sach_khach_hang = []

    for user in users:
        

        don_hang_qs = Order.objects.filter(user=user)

        so_don_hang = don_hang_qs.count()
        tong_chi_tieu = don_hang_qs.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        if not user.is_active:
            trang_thai = 'ngung_hoat_dong'
        elif tong_chi_tieu >= 1000000:
            trang_thai = 'vip'
        elif so_don_hang >= 2:
            trang_thai = 'than_thiet'
        else:
            trang_thai = 'khach_moi'

        tinh_thanh = user.address if user.address else 'Chưa cập nhật'
        ho_ten = user.get_full_name().strip() if user.get_full_name().strip() else user.username
        email = user.email if user.email else 'Chưa cập nhật'
        so_dien_thoai = user.phone if user.phone else 'Chưa cập nhật'

        khach_hang = {
            'id': user.id,
            'ho_ten': ho_ten,
            'ky_tu_dai_dien': ho_ten[:1].upper() if ho_ten else 'K',
            'ma_khach_hang': f'KH{user.id:03d}',
            'email': email,
            'so_dien_thoai': so_dien_thoai,
            'tinh_thanh': tinh_thanh,
            'so_don_hang': so_don_hang,
            'tong_chi_tieu': tong_chi_tieu,
            'tong_chi_tieu_hien_thi': f"{int(tong_chi_tieu):,}".replace(",", ".") + "đ",
            'trang_thai': trang_thai,
            'ngay_tham_gia': user.date_joined,
            'ngay_tham_gia_hien_thi': user.date_joined.strftime('%d/%m/%Y'),
        }

        danh_sach_khach_hang.append(khach_hang)

    if q:
        q_lower = q.lower()
        danh_sach_khach_hang = [
            kh for kh in danh_sach_khach_hang
            if q_lower in kh['ho_ten'].lower()
            or q_lower in kh['ma_khach_hang'].lower()
            or q_lower in kh['email'].lower()
            or q_lower in kh['so_dien_thoai'].lower()
        ]

    if status != 'tat_ca':
        danh_sach_khach_hang = [
            kh for kh in danh_sach_khach_hang
            if kh['trang_thai'] == status
        ]

    if sort == 'cu_nhat':
        danh_sach_khach_hang.sort(key=lambda x: x['ngay_tham_gia'])
    elif sort == 'ten_a_z':
        danh_sach_khach_hang.sort(key=lambda x: x['ho_ten'].lower())
    elif sort == 'nhieu_don_nhat':
        danh_sach_khach_hang.sort(key=lambda x: x['so_don_hang'], reverse=True)
    elif sort == 'chi_tieu_cao_nhat':
        danh_sach_khach_hang.sort(key=lambda x: x['tong_chi_tieu'], reverse=True)
    else:
        danh_sach_khach_hang.sort(key=lambda x: x['ngay_tham_gia'], reverse=True)

    tong_khach_hang = len(danh_sach_khach_hang)
    khach_moi = len([kh for kh in danh_sach_khach_hang if kh['trang_thai'] == 'khach_moi'])
    khach_hang_than_thiet = len([kh for kh in danh_sach_khach_hang if kh['trang_thai'] == 'than_thiet'])
    khach_vip = len([kh for kh in danh_sach_khach_hang if kh['trang_thai'] == 'vip'])

    context = {
        'active_page': 'customers',
        'tong_khach_hang': tong_khach_hang,
        'khach_moi': khach_moi,
        'khach_hang_than_thiet': khach_hang_than_thiet,
        'khach_vip': khach_vip,
        'danh_sach_khach_hang': danh_sach_khach_hang,
        'bo_loc': {
            'q': q,
            'status': status,
            'sort': sort,
        }
    }

    return render(request, 'dashboard/customers.html', context)

@login_required(login_url='login')
def report_view(request):
    orders = Order.objects.all()

    # chỉ tính đơn thành công
    completed_orders = orders.filter(status='completed')

    total_orders = completed_orders.count()

    total_revenue = completed_orders.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    formatted_revenue = f"{int(total_revenue):,}".replace(",", ".")

    # tỷ lệ huỷ
    total_all = orders.count()
    total_cancelled = orders.filter(status='cancelled').count()

    cancel_rate = 0
    if total_all > 0:
        cancel_rate = round((total_cancelled / total_all) * 100, 1)

    context = {
        'total_revenue': formatted_revenue,
        'total_orders': total_orders,
        'cancel_rate': cancel_rate,
    }

    return render(request, 'dashboard/report.html', context)


@login_required(login_url='login')
def order_list_view(request):
    orders = Order.objects.select_related('user').all().order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)


@login_required(login_url='login')
def order_detail_view(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user'), id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        valid_transitions = {
            'new': ['pending', 'cancelled'],
            'pending': ['shipping', 'cancelled'],
            'shipping': ['completed'],
            'completed': [],
            'cancelled': [],
        }
        print("METHOD:", request.method)
        print("CURRENT:", order.status)
        print("POST STATUS:", request.POST.get("status"))
        if new_status and new_status in valid_transitions.get(order.status, []):
            order.status = new_status
            order.save()

        return redirect('order_detail', order_id=order.id)

    context = {
        'order': order
    }
    return render(request, 'dashboard/order_detail.html', context)

def product_list_view(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "dashboard/products.html", {"products": products})


def product_create_view(request):
    return render(request, "dashboard/product_create.html")


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "dashboard/product_edit.html", {"product": product})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("product_list")


def dashboard_home(request):
    return render(request, 'dashboard/dashboard.html')

def dashboard_products(request):
    return render(request, 'dashboard/products.html')

def dashboard_orders(request):
    return render(request, 'dashboard/orders.html')


def dashboard_reports(request):
    return render(request, 'dashboard/report.html')

def dashboard_permissions(request):
    return render(request, 'dashboard/permissions.html')