from django.shortcuts import render, redirect, get_object_or_404
from .form import Order_Servises_form
from .models import Servises, Employee, Order
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url='login')
def servises_page(request):
    items = Servises.objects.all()
    # Базовий запит — беремо всіх
    employees = Employee.objects.select_related('profession').all()
    
    # Отримуємо ID вибраної послуги з URL (наприклад: ?service_filter=2)
    chosen_service_id = request.GET.get('service_filter')
    
    if chosen_service_id:
        # Фільтруємо працівників, у яких ID професії збігається з вибраним
        employees = employees.filter(profession_id=chosen_service_id)

    return render(request, 'servises/servises.html', {
        'items': items,
        'employees': employees,
        'chosen_service_id': chosen_service_id, # Передаємо назад, щоб зберегти вибір у селекті
    })


@login_required(login_url='login')
def order_page(request, service_id=None, employee_id=None):
    initial_data = {}
    
    # Якщо прийшли динамічні параметри з URL — підтягуємо дефолтні значення для форми
    if service_id and employee_id:
        service_obj = get_object_or_404(Servises, id=service_id)
        employee_obj = get_object_or_404(Employee, id=employee_id)
        initial_data = {
            'service': service_obj,
            'employee': employee_obj
        }

    if request.method == 'POST':
        form = Order_Servises_form(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('servises')
    else:
        # Передаємо initial дані у форму, щоб селекти стали вибраними самі!
        form = Order_Servises_form(initial=initial_data)
    
    return render(request, 'servises/order_servises.html', {'form': form})