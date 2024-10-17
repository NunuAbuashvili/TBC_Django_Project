from django.urls import path
from . import views

app_name='store'

urlpatterns = [
    path('', views.store_homepage, name='store_homepage'),
    path('products/', views.list_products, name='products'),
    path('categories/', views.list_categories, name='product_categories'),
    path('category/', views.categories_list_view, name='categories_list'),
    path('category/<int:category_id>/products/', views.category_detailed_view, name='category_products'),
    path('category/<int:category_id>/products/<int:product_id>/', views.product_detailed_view, name='product_page'),
]
