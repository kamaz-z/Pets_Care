from django.shortcuts import render, redirect
from .form import Order_Servises_form
from django.contrib import messages
from .models import Servises

def servises_page(request):
    # Отримуємо всі послуги з бази даних
    items = Servises.objects.all()
    return render(request, 'servises/servises.html', {'items': items})

def order_page(request):
    if request.method == 'POST':
        form = Order_Servises_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дякуємо! Замовлення прийнято, ми вам зателефонуємо.')
            return redirect('servises')
    else:
        form = Order_Servises_form()
    
    return render(request, 'servises/order_servises.html', {'form': form})