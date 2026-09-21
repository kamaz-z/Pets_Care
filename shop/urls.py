from django.urls import path
from . import views

urlpatterns = [
    path('',views.shop_page, name='shop_page'),
    path('cart_page/',views.cart_page,name ='cart_page'),
    path('create-order/', views.create_order, name='create_order'),
    path('api/novapost/settlements/', views.np_settlements, name='np_settlements'),
    path('api/novapost/divisions/<int:settlement_id>/', views.np_divisions, name='np_divisions'),
]
