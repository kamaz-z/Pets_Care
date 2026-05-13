from django.db import models

class Type_OF_PETS(models.Model):
    type = models.CharField(verbose_name="тип тварини", max_length=50)
    def __str__(self):
        return self.type
    class Meta:
        verbose_name="Тип тварини"



class Pets(models.Model):
    type_pets = models.ForeignKey(Type_OF_PETS,on_delete=models.CASCADE,verbose_name='тип тварини')
    name = models.CharField(max_length=40,verbose_name="ім'я")
    age = models.PositiveIntegerField(verbose_name="вік")
    weight = models.PositiveIntegerField(verbose_name='вага')
    passport_number = models.PositiveIntegerField(verbose_name="номер паспорта")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Тварини"


     
