from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_page_view, name='order_page_view'),
    path('history/', views.order_history, name='order_history'),
]
