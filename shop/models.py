from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=50)
    count = models.SmallIntegerField(default=0)
    discrp = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    img  = models.ImageField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="Товар"

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупець")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    phone = models.CharField(max_length=15, verbose_name="Номер телефону")
    address = models.CharField(max_length=255, verbose_name="Адреса доставки")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення {self.id} - {self.product.name}"

    class Meta:
        verbose_name = "Замовлення"