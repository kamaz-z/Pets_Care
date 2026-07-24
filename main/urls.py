from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name="home"),
    path('regiser/',views.register, name = "register"),
    path('login/',views.login_user, name= "login"),
    path('register_pets/',views.register_pets, name="register_pets"),
    path('logout/',views.user_logout, name='logout'),
    path('find_pets',views.find_pets, name='find_pets'),
    path('AI',views.ai_chat_page, name = 'ai_chat'),
    path('find_home',views.find_home, name='find_home'),
    path('pricing',views.pricing, name = 'pricing'),
    path('map',views.map, name = 'map')
]
