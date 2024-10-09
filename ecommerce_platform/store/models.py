from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(verbose_name="product description", blank=True, null=True)
    manufacturer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('Category', related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True
    )
    description = models.TextField(verbose_name="category description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
