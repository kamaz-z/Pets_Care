from django.db import models
from django.contrib.auth.models import User

# Це список самих послуг (адмін створює їх)
class Servises(models.Model):
    name = models.CharField(max_length=50)
    discrp = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='services/')
    
    def __str__(self):
        return self.name

# Це таблиця замовлень, куди падають дані від клієнтів
class Order(models.Model):
    service = models.ForeignKey(Servises, on_delete=models.CASCADE, verbose_name="Послуга")
    customer_phone = models.CharField(max_length=15, verbose_name="Номер телефону")
    order_date = models.DateField(verbose_name="Дата візиту")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення на {self.order_date} - {self.customer_phone}"