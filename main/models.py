from django.db import models
from django.contrib.auth.models import User
class Type_OF_PETS(models.Model):
    type = models.CharField(verbose_name="тип тварини", max_length=50)
    def __str__(self):
        return self.type
    class Meta:
        verbose_name="Тип тварини"



class Pets(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type_pets = models.ForeignKey(Type_OF_PETS,on_delete=models.CASCADE,verbose_name='тип тварини')
    poroda = models.CharField(max_length=30,verbose_name='Порода',default='золотий ретривер')
    name = models.CharField(max_length=40,verbose_name="ім'я")
    age = models.PositiveIntegerField(verbose_name="вік")
    weight = models.FloatField(verbose_name='вага')
    passport_number = models.PositiveIntegerField(verbose_name="номер паспорта")
    img = models.ImageField(upload_to='pets_photos/', verbose_name="Фото улюбленця", null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Тварини"

class find_Pets(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Розшукується'),
        ('found', 'Знайдено'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Автор')
    pet_name = models.CharField(max_length=80,verbose_name='кличка')
    pet_type = models.CharField(max_length=100,verbose_name='Вид тварини')
    last_location = models.CharField(max_length=200,verbose_name="Останнє місцезнаходження")
    discrp = models.CharField(max_length=300, verbose_name='Опис')
    contacts = models.CharField(max_length=100, verbose_name="Контакти")
    img = models.ImageField(upload_to='lost_pets/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='lost',verbose_name='статус')
    def __str__(self):
        return f"{self.pet_name} ({self.get_status_display()})"

    class Meta:
        verbose_name="Зниклі тварини"

class Find_Home(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я тваринки")
    type_pets = models.CharField(max_length=100, verbose_name="Тип тваринки")
    age = models.PositiveIntegerField(verbose_name="вік")
    img = models.ImageField(upload_to='find_home/', verbose_name="Фото улюбленця", null=True, blank=True)
    discp = models.CharField(max_length=300,verbose_name='Опис тваринки')
    contact = models.CharField(max_length=50, verbose_name='Контакт куди телефонувати')


    class Meta:
        verbose_name="Шукають домівку"