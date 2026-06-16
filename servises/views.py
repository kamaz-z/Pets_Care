from django.shortcuts import render, redirect
from .form import Order_Servises_form
from django.contrib import messages
from .models import Servises,Order
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def servises_page(request):
    # Отримуємо всі послуги з бази даних
    items = Servises.objects.all()
    return render(request, 'servises/servises.html', {'items': items})
@login_required(login_url='login')
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

def order_msg(request):
    items_order = Order.objects.all()
    now_t =  timezone.now()

    for date in items_order:
        if now_t - date.order_date  <= timedelta(hours=1):
            print("надсиалння повідомлення")
        elif now_t - date.order_date  <= timedelta(hours=5):
            print("надсиалння повідомлення")    
            gmail_msg(1)
        elif now_t - date.order_date <= timedelta(days=1):
            print("надсиалння повідомлення")
            gmail_msg(24)
       
    return render(request,"servises/order_servises.html")

def gmail_msg(time):
    user = User
    items = Order.objects.all()
    for item in items:
        print(item.service)
    try:
        msg = MIMEText(f'{user.username} Вітаю до вашого запису залишилось {time} годин \n на запис до {item.service}', 'plain', 'utf-8')
        msg['Subject'] = f'Запис до {item.service}'
        msg['From'] = 'vladyslav.hadiak.kb.2024@lpnu.ua'
        msg['To'] = user.email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('vladyslav.hadiak.kb.2024@lpnu.ua', 'lzjn iquu xjlz korb')
        server.sendmail('vladyslav.hadiak.kb.2024@lpnu.ua', user.email, msg.as_string())
        server.quit()
    except Exception as e:
        print(e)
    return time