from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name="home"),
    path('regiser/',views.register,name = "register"),
    path('register_pets/',views.register_pets,name="register_pets"),
]
