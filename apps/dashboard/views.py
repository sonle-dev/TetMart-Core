import json
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from products.models import Product
from orders.models import Order
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from tetmart.permission_utils import PERMISSION_PAGE_PERMS, permission_gate

User = get_user_model()

def has_permission_page_access(user):
    return user.is_authenticated and (
        user.is_superuser or user.has_perm('auth.view_permission_page')
    )
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
def customer_create(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        address = request.POST.get('address', '').strip()

        if not username or not phone:
            messages.error(request, 'Vui lòng nhập đầy đủ họ tên và số điện thoại.')
            return redirect('customer_create')

        User.objects.create_user(
            username=username,
            email=email,
            password='123456',
            phone=phone,
            address=address or city,
            is_customer=True
        )

        messages.success(request, 'Thêm khách hàng thành công.')
        return redirect('dashboard_customers')

    return render(request, 'dashboard/customer_create.html', {
        'active_page': 'customers'
    })

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

def _get_role_level(group_name):
    ten = (group_name or '').lower()

    if 'admin' in ten:
        return 'Cao', 'danger'
    if 'đơn hàng' in ten or 'order' in ten or 'vận hành' in ten:
        return 'Vận hành', 'warning'
    if 'sản phẩm' in ten or 'product' in ten or 'danh mục' in ten:
        return 'Danh mục', 'primary'
    if 'cskh' in ten or 'khách hàng' in ten or 'customer' in ten:
        return 'Chăm sóc', 'success'
    if 'báo cáo' in ten or 'report' in ten:
        return 'Báo cáo', 'secondary'

    return 'Khác', 'secondary'


def _group_permission_module(permission):
    app_label = permission.content_type.app_label
    codename = permission.codename.lower()

    if app_label in ['dashboard'] or 'dashboard' in codename:
        return 'Dashboard', 'Truy cập trang tổng quan và số liệu chính.'

    if app_label in ['orders', 'order'] or 'order' in codename:
        return 'Đơn hàng', 'Quản lý toàn bộ quy trình đơn hàng.'

    if app_label in ['products', 'product', 'catalog'] or 'product' in codename:
        return 'Sản phẩm', 'Thao tác đầy đủ với sản phẩm.'

    if app_label in ['users', 'user'] or 'customer' in codename:
        return 'Khách hàng', 'Xem hồ sơ khách hàng và hỗ trợ đơn hàng.'

    if 'permission' in codename or 'group' in codename or app_label == 'auth':
        return 'Phân quyền', 'Thiết lập vai trò và gán quyền cho thành viên.'

    return 'Khác', 'Các quyền khác trong hệ thống.'


def _pretty_permission_name(permission):
    action_map = {
        'add': 'Thêm',
        'change': 'Sửa',
        'delete': 'Xóa',
        'view': 'Xem',
    }

    parts = permission.codename.split('_', 1)

    if len(parts) == 2 and parts[0] in action_map:
        return f"{action_map[parts[0]]} {parts[1].replace('_', ' ')}"

    return permission.name


def _serialize_group(group):
    level, level_class = _get_role_level(group.name)

    members = []
    for user in group.user_set.all().order_by('username'):
        display_name = user.get_full_name().strip() if user.get_full_name().strip() else user.username
        members.append({
            'name': display_name,
            'email': user.email or 'Chưa cập nhật'
        })

    module_map = {}

    permissions = group.permissions.select_related('content_type').all().order_by(
        'content_type__app_label', 'codename'
    )

    for permission in permissions:
        module_title, module_description = _group_permission_module(permission)

        if module_title not in module_map:
            module_map[module_title] = {
                'title': module_title,
                'description': module_description,
                'permissions': []
            }

        module_map[module_title]['permissions'].append({
            'label': _pretty_permission_name(permission),
            'enabled': True
        })

    return {
        'id': f'group_{group.id}',
        'group_id': group.id,
        'name': group.name,
        'level': level,
        'levelClass': level_class,
        'description': f'Vai trò {group.name} trong hệ thống quản trị.',
        'members': members,
        'modules': list(module_map.values())
    }

@permission_gate(*PERMISSION_PAGE_PERMS)
def dashboard_permissions(request):
    groups = Group.objects.prefetch_related('permissions', 'user_set').all()

    role_data = []
    for g in groups:
        members = [
            {
                'id': u.id,
                'name': u.username,
                'email': u.email or 'Chưa cập nhật'
            }
            for u in g.user_set.filter(is_staff=True)
        ]

        group_permission_codes = set(
            g.permissions.values_list('codename', flat=True)
        )

        permission_modules = [
            {
                'title': 'Dashboard',
                'description': 'Truy cập trang tổng quan và số liệu chính.',
                'permissions': [
                    ('view_dashboard', 'Xem dashboard'),
                ],
            },
            {
                'title': 'Đơn hàng',
                'description': 'Quản lý toàn bộ quy trình đơn hàng.',
                'permissions': [
                    ('view_order', 'Xem danh sách đơn'),
                    ('update_order_status', 'Cập nhật trạng thái đơn'),
                    ('export_order', 'Xuất danh sách đơn'),
                    ('cancel_order', 'Hủy đơn'),
                ],
            },
            {
                'title': 'Sản phẩm',
                'description': 'Thao tác đầy đủ với sản phẩm.',
                'permissions': [
                    ('view_product', 'Xem sản phẩm'),
                    ('add_product', 'Thêm sản phẩm'),
                    ('change_product', 'Sửa sản phẩm'),
                    ('delete_product', 'Xóa sản phẩm'),
                    ('hide_product', 'Ẩn / hiện sản phẩm'),
                ],
            },
            {
                'title': 'Khách hàng',
                'description': 'Xem hồ sơ khách hàng và hỗ trợ đơn hàng.',
                'permissions': [
                    ('view_customer_list', 'Xem danh sách khách hàng'),
                    ('view_customer_detail', 'Xem chi tiết khách hàng'),
                    ('create_customer', 'Thêm khách hàng mới'),
                    ('lock_customer', 'Khóa khách hàng'),
                ],
            },
            {
                'title': 'Báo cáo',
                'description': 'Xem báo cáo doanh thu.',
                'permissions': [
                    ('view_revenue_report', 'Xem báo cáo doanh thu'),
                ],
            },
            {
                'title': 'Phân quyền',
                'description': 'Thiết lập vai trò và gán quyền cho thành viên.',
                'permissions': [
                    ('view_permission_page', 'Xem trang phân quyền'),
                    ('create_role', 'Tạo vai trò mới'),
                    ('assign_role_member', 'Gán vai trò cho thành viên'),
                ],
            },
        ]

        modules = []

        for module in permission_modules:
            permission_items = []

            for codename, label in module['permissions']:
                permission_items.append({
                    'code': codename,
                    'label': label,
                    'enabled': codename in group_permission_codes,
                })

            modules.append({
                'title': module['title'],
                'description': module['description'],
                'permissions': permission_items,
            })

        level = 'Khác'
        level_class = 'secondary'
        group_name_lower = g.name.lower()

        if 'admin' in group_name_lower:
            level = 'Cao'
            level_class = 'danger'
        elif 'đơn hàng' in group_name_lower or 'order' in group_name_lower:
            level = 'Vận hành'
            level_class = 'warning'
        elif 'sản phẩm' in group_name_lower or 'product' in group_name_lower:
            level = 'Danh mục'
            level_class = 'primary'
        elif 'cskh' in group_name_lower or 'khách hàng' in group_name_lower:
            level = 'Chăm sóc'
            level_class = 'success'
        elif 'báo cáo' in group_name_lower or 'report' in group_name_lower:
            level = 'Báo cáo'
            level_class = 'secondary'

        role_data.append({
            'id': f'group_{g.id}',
            'name': g.name,
            'level': level,
            'levelClass': level_class,
            'description': f'Vai trò {g.name} trong hệ thống quản trị.',
            'members': members,
            'modules': modules
        })

    user_pool = [
        {
            'id': u.id,
            'name': u.username,
            'email': u.email or 'Chưa cập nhật'
        }
        for u in User.objects.all().order_by('username')
    ]

    print('user_pool_json =', json.dumps(user_pool, ensure_ascii=False))
    print('role_data_json =', json.dumps(role_data, ensure_ascii=False))

    return render(request, 'dashboard/permissions.html', {
        'user_pool_json': json.dumps(user_pool, ensure_ascii=False),
        'role_data_json': json.dumps(role_data, ensure_ascii=False),
    })

@require_POST
@permission_gate(*PERMISSION_PAGE_PERMS)
def add_role_member(request):
    try:
        data = json.loads(request.body)
        role_id = data.get('role_id')
        user_id = data.get('user_id')

        if not role_id or not user_id:
            return JsonResponse({
                'success': False,
                'message': 'Thiếu dữ liệu thêm thành viên.'
            }, status=400)

        if str(role_id).startswith('group_'):
            role_id = str(role_id).replace('group_', '')

        group = get_object_or_404(Group, id=role_id)
        user = get_object_or_404(User, id=user_id)
        if not user:
            return JsonResponse({
                'success': False,
                'message': 'Không tìm thấy tài khoản này.'
            }, status=404)

        if group.user_set.filter(id=user.id).exists():
            return JsonResponse({
                'success': False,
                'message': f'{user.username} đã thuộc vai trò {group.name}.'
            }, status=400)

        user.groups.add(group)

        if not user.is_staff:
            user.is_staff = True
            user.save(update_fields=['is_staff'])

        return JsonResponse({
            'success': True,
            'message': f'{user.username} đã được thêm vào vai trò {group.name}.',
            'member': {
                'name': user.username,
                'email': user.email or 'Chưa cập nhật'
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu gửi lên không hợp lệ.'
        }, status=400)

@require_POST
@permission_gate(*PERMISSION_PAGE_PERMS)
def remove_role_member(request):
    try:
        data = json.loads(request.body)
        role_id = data.get('role_id')
        user_id = data.get('user_id')

        if not role_id or not user_id:
            return JsonResponse({
                'success': False,
                'message': 'Thiếu dữ liệu xóa thành viên.'
            }, status=400)

        if str(role_id).startswith('group_'):
            role_id = str(role_id).replace('group_', '')

        group = get_object_or_404(Group, id=role_id)
        user = get_object_or_404(User, id=user_id)
        if not user:
            return JsonResponse({
                'success': False,
                'message': 'Không tìm thấy tài khoản này.'
            }, status=404)

        if not group.user_set.filter(id=user.id).exists():
            return JsonResponse({
                'success': False,
                'message': f'{user.username} không thuộc vai trò {group.name}.'
            }, status=400)

        user.groups.remove(group)

        if not user.is_superuser and not user.groups.exists():
            user.is_staff = False
            user.save(update_fields=['is_staff'])

        return JsonResponse({
            'success': True,
            'message': f'{user.username} đã được gỡ khỏi vai trò {group.name}.'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu gửi lên không hợp lệ.'
        }, status=400)