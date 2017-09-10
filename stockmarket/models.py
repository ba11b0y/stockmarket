from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Stock(models.Model):

    name = models.CharField(max_length=10)
    current_price = models.FloatField(default=0)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    stocks = models.ManyToManyField(Stock)
    total_fund = models.FloatField(default=500000.0)
    def __str__(self):
        return self.username

class Buy_Data(models.Model):
    stock = models.ForeignKey(Stock)
    user = models.ForeignKey(CustomUser)
    price = ArrayField(models.FloatField(default=0.0))
    quantity = ArrayField(models.IntegerField(default=0))
    average_price = models.FloatField(default=0.0)
    def get_average_price(self):
        tprice=0
        for i in range(len(self.price)):
            tprice+=(self.quantity[i]*self.price[i])
        quantity = sum(self.quantity)
        if quantity==0:
            avg = 0
            return avg
        avg = round(tprice/quantity,2)
        return avg

    def __str__(self):
        return self.user.username+ " bought "+self.stock.name



