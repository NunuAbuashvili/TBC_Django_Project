from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_homepage, name='store_homepage'),
    path('products/', views.store_products, name='store_products'),
]
