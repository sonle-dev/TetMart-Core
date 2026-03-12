from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại", blank=True, null=True)
    address = models.TextField(verbose_name="Địa chỉ giao hàng", blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Ảnh đại diện")
    
    
    is_customer = models.BooleanField(default=True, verbose_name="Là khách hàng")
    
    def __str__(self):
        return self.username