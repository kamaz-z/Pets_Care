from django.urls import path
from . import views

urlpatterns = [
    path('', views.servises_page, name='servises'),
    # Старий маршрут + новий динамічний маршрут
    path('servises_order/', views.order_page, name='order_service'),
    path('servises_order/<int:service_id>/<int:employee_id>/', views.order_page, name='order_service_with_employee'),
]