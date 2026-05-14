from . import views
from django.urls import path

urlpatterns = [
    path('',views.servises_page,name='servises'),
    path('servises_order',views.order_page,name='order_service')

]
