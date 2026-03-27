from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Đơn mới'),
        ('pending', 'Chờ xử lý'),
        ('shipping', 'Đang giao'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    full_name = models.CharField(max_length=100, default='', verbose_name="Họ tên người nhận")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=255, verbose_name="Địa chỉ giao hàng")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tổng tiền")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")

    def __str__(self):
        return f"Đơn hàng #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total(self):
        return self.price * self.quantity