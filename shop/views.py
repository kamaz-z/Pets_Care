from django.shortcuts import render
from .models import Product

def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})