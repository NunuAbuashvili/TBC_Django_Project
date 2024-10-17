from decimal import Decimal
from typing import Optional

from django.contrib import admin
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = ('name', 'manufacturer', 'price', 'stock_quantity', 'total_value')
    list_filter = ('is_active', 'manufacturer', 'created_at', 'updated_at')
    search_fields = ('name', 'categories__name')
    search_help_text = 'Search by product name or category'
    list_editable = ('stock_quantity', 'price')
    ordering = ('stock_quantity',)
    prefetch_related = ('categories',)
    view_on_site = True
    save_on_top = True
    list_per_page = 10

    @admin.display(description='Total Value')
    def total_value(self, instance: Product) -> Decimal:
        """
        Calculates the total value of product.

        Args:
            instance: The Product instance.

        Returns:
            Decimal: Total value (price * quantity).
        """
        return instance.stock_quantity * instance.price

    def view_on_site(self, instance: Product) -> str:
        """
        Generates the URL for viewing the product.

        Args:
            instance: The Product instance.

        Returns:
            str: URL for viewing the product on the site.
        """
        root_category = instance.categories.first().get_root()
        return f'http://localhost:8000/category/{root_category.id}/products/{instance.id}/'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ('name', 'root_category', 'category_products', 'tree_products')
    search_fields = ('name',)
    search_help_text = 'Search by category name'
    ordering = ('name',)
    save_on_top = True
    list_per_page = 10

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """
        Enhance the base queryset with product counts.

        Args:
            request: The HTTP request object.

        Returns:
            QuerySet: Enhanced queryset with product counts.
        """
        queryset_for_count = super().get_queryset(request)

        # Add count of products directly in this category
        queryset_for_count = Category.objects.add_related_count(
            queryset_for_count, Product, 'categories',
            'products_cumulative_count',cumulative=True
        )

        # Add count of products in this category and all descendants
        queryset_for_count = Category.objects.add_related_count(
            queryset_for_count, Product, 'categories',
            'products_count', cumulative=False
        )

        return queryset_for_count

    @admin.display(description='Products count (for this specific category)')
    def category_products(self, instance) -> int:
        """
        Get the number of products directly in this category.

        Args:
            instance: The Category instance.

        Returns:
            int: Number of products in this category.
        """
        return instance.products_count

    @admin.display(description='Products count (in tree)')
    def tree_products(self, instance) -> int:
        """
        Get the total number of products in a main category,
        including its descendants.

        Args:
            instance: The Category instance.

        Returns:
            int: Total number of products in the main category tree.
        """
        return instance.products_cumulative_count

    @admin.display(description='Main category')
    def root_category(self, instance) -> Optional[str]:
        """
        Get the root category name with caching.

        Args:
            instance: The Category instance.

        Returns:
            Optional[str]: Root category name or None if the instance is already a root.
        """
        if instance.is_root_node():
            return None

        cache_key = f'root_name:{instance.tree_id}'
        root_category_name = cache.get(cache_key)
        if not root_category_name:
            root_category_name= instance.get_root().name
            cache.set(cache_key, root_category_name, timeout=3600)

        return root_category_name
