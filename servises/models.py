from django.db import models
from django.contrib.auth.models import User

class Servises(models.Model):
    name = models.CharField(max_length=50)
    discrp = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    profession = models.ForeignKey(
        Servises,
        on_delete=models.CASCADE
    )
    descrp = models.CharField(max_length=400,verbose_name='ваш опис',default='я працівник')
    price = models.PositiveIntegerField(default=1000, verbose_name='ціна')
    img = models.ImageField(upload_to='servises/',null=True,blank=True,verbose_name='фото співробітника')


    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='servises_user'
    )

    service = models.ForeignKey(
        Servises,
        on_delete=models.CASCADE
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    order_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} -> {self.service}"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    
    # Текст повідомлення
    text = models.TextField() # Використовуємо TextField, бо відповіді ШІ бувають довшими за 400 символів
    
    # Хто відправив: True — користувач, False — штучний інтелект (Gemini)
    is_from_user = models.BooleanField(default=True)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = "User" if self.is_from_user else "AI"
        return f"{self.user.username} | {sender}: {self.text[:30]}..."