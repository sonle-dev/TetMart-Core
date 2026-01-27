from django.db import models

#  Bảng Danh Mục 
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, verbose_name="Link SEO (Slug)") 


    def __str__(self):
        return self.name

#  Bảng Sản Phẩm
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Danh mục")
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(unique=True, verbose_name="Link SEO (Slug)")
    image = models.ImageField(upload_to='products/', verbose_name="Ảnh sản phẩm", blank=True, null=True)
    description = models.TextField(verbose_name="Mô tả", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá bán (VNĐ)")
    stock = models.IntegerField(default=0, verbose_name="Tồn kho")
    is_active = models.BooleanField(default=True, verbose_name="Đang bán")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    def __str__(self):
        return self.name