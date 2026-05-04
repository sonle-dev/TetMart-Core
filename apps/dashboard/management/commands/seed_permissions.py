from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from orders.models import Order
from products.models import Product, Category


class Command(BaseCommand):
    help = "Seed roles and permissions for dashboard permissions page"

    def handle(self, *args, **options):
        User = get_user_model()

        group_names = [
            'Admin tổng',
            'Quản lý đơn hàng',
            'Quản lý sản phẩm',
            'CSKH',
            'Nhân viên báo cáo',
        ]

        groups = {}
        for name in group_names:
            group, _ = Group.objects.get_or_create(name=name)
            groups[name] = group

       
        order_ct = ContentType.objects.get_for_model(Order)
        product_ct = ContentType.objects.get_for_model(Product)
        category_ct = ContentType.objects.get_for_model(Category)
        user_ct = ContentType.objects.get_for_model(User)
        group_ct = ContentType.objects.get_for_model(Group)


        custom_permissions = [
            # Dashboard
            ('view_dashboard', 'Xem dashboard', group_ct),
            ('view_revenue_dashboard', 'Xem số liệu doanh thu', group_ct),

            # Orders extra
            ('update_order_status', 'Cập nhật trạng thái đơn', order_ct),
            ('export_order', 'Xuất danh sách đơn', order_ct),
            ('cancel_order', 'Hủy đơn', order_ct),

            # Product extra
            ('hide_product', 'Ẩn / hiện sản phẩm', product_ct),

            # Customers extra
            ('view_customer_list', 'Xem danh sách khách hàng', user_ct),
            ('view_customer_detail', 'Xem chi tiết khách hàng', user_ct),
            ('create_customer', 'Thêm khách hàng mới', user_ct),
            ('lock_customer', 'Khóa khách hàng', user_ct),

            # Reports
            ('view_report', 'Xem báo cáo', group_ct),
            ('export_report', 'Xuất báo cáo', group_ct),
            ('view_revenue_report', 'Xem báo cáo doanh thu', group_ct),

            # Permissions
            ('view_permission_page', 'Xem trang phân quyền', group_ct),
            ('create_role', 'Tạo vai trò mới', group_ct),
            ('assign_role_member', 'Gán vai trò cho thành viên', group_ct),
        ]

        for codename, name, content_type in custom_permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )

        
        def perm(codename, content_type):
            return Permission.objects.get(codename=codename, content_type=content_type)

       
        # Admin tổng
        admin_permissions = [
            perm('view_dashboard', group_ct),

            # Đơn hàng
            perm('view_order', order_ct),
            perm('update_order_status', order_ct),
            perm('export_order', order_ct),
            perm('cancel_order', order_ct),

            # Khách hàng
            perm('view_customer_list', user_ct),
            perm('view_customer_detail', user_ct),
            perm('create_customer', user_ct),
            perm('lock_customer', user_ct),

            # Sản phẩm
            perm('view_product', product_ct),
            perm('add_product', product_ct),
            perm('change_product', product_ct),
            perm('delete_product', product_ct),
            perm('hide_product', product_ct),

            # Báo cáo
            perm('view_dashboard', group_ct),
            perm('view_revenue_report', group_ct),


            # Phân quyền
            perm('view_permission_page', group_ct),
            perm('create_role', group_ct),
            perm('assign_role_member', group_ct),
        ]
        groups['Admin tổng'].permissions.set(admin_permissions)

        # Quản lý đơn hàng
        order_permissions = [
            perm('view_order', order_ct),
            perm('update_order_status', order_ct),
            perm('cancel_order', order_ct),
            perm('export_order', order_ct),

            perm('view_customer_list', user_ct),
            perm('lock_customer', user_ct),
        ]
        groups['Quản lý đơn hàng'].permissions.set(order_permissions)

        # Quản lý sản phẩm
        product_permissions = [
            perm('view_product', product_ct),
            perm('add_product', product_ct),
            perm('change_product', product_ct),
            perm('delete_product', product_ct),
            perm('hide_product', product_ct),

            perm('view_report', group_ct),
            perm('export_report', group_ct),
        ]
        groups['Quản lý sản phẩm'].permissions.set(product_permissions)

        # CSKH
        customer_permissions = [
            perm('view_customer_list', user_ct),
            perm('view_customer_detail', user_ct),
            perm('create_customer', user_ct),
            perm('lock_customer', user_ct),

            perm('view_order', order_ct),
            perm('update_order_status', order_ct),
        ]
        groups['CSKH'].permissions.set(customer_permissions)

        # Nhân viên báo cáo
        report_permissions = [
            perm('view_dashboard', group_ct),
            perm('view_revenue_report', group_ct),
            perm('export_report', group_ct),
        ]
        groups['Nhân viên báo cáo'].permissions.set(report_permissions)

        self.stdout.write(self.style.SUCCESS('Seed roles and permissions successfully.'))