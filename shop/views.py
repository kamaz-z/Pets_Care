from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})  