from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_homepage, name='store_homepage'),
    path('products/', views.list_products, name='products'),
    path('categories/', views.show_categories, name='product_categories'),
]
