from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


DASHBOARD_PERMS = (
    'auth.view_dashboard',
    'auth.view_revenue_dashboard',
)

ORDER_PERMS = (
    'orders.view_order',
    'orders.update_order_status',
    'orders.export_order',
    'orders.cancel_order',
)

CUSTOMER_PERMS = (
    'users.view_customer_list',
    'users.view_customer_detail',
    'users.create_customer',
    'users.lock_customer',
)

PRODUCT_PERMS = (
    'products.view_product',
    'products.add_product',
    'products.change_product',
    'products.delete_product',
    'products.hide_product',
)

REPORT_PERMS = (
    'auth.view_report',
    'auth.export_report',
    'auth.view_revenue_report',
)

PERMISSION_PAGE_PERMS = (
    'auth.view_permission_page',
    'auth.create_role',
    'auth.assign_role_member',
)


def has_any_perm(user, perms):
    return user.is_authenticated and (
        user.is_superuser or any(user.has_perm(perm) for perm in perms)
    )


def first_allowed_dashboard_name(user):
    checks = [
        (DASHBOARD_PERMS, 'dashboard'),
        (ORDER_PERMS, 'dashboard_orders'),
        (CUSTOMER_PERMS, 'dashboard_customers'),
        (PRODUCT_PERMS, 'dashboard_products'),
        (REPORT_PERMS, 'report'),
        (PERMISSION_PAGE_PERMS, 'permissions'),
    ]

    for perms, url_name in checks:
        if has_any_perm(user, perms):
            return url_name

    return None


def permission_gate(*perms):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def _wrapped_view(request, *args, **kwargs):
            if has_any_perm(request.user, perms):
                return view_func(request, *args, **kwargs)

            messages.error(request, 'Bạn không có quyền truy cập trang này.')
            target = first_allowed_dashboard_name(request.user)
            return redirect(target or 'home')

        return _wrapped_view

    return decorator