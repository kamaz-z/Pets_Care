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
