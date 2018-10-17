from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Stock(models.Model):

    name = models.CharField(max_length=10)
    ltp = models.FloatField()
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    total_fund = models.FloatField(default=500000.0)
    def __str__(self):
        return self.username

class Order(models.Model):

    trader = models.ForeignKey(CustomUser, related_name='orders')
    stock = models.ForeignKey(Stock)
    order_type = models.CharField(max_length=4)
    quantity = models.IntegerField()
    amount = models.FloatField()

    def __str__(self):
        return self.trader.username+" - "+self._type

    def save(self, *args, **kwargs):
        amount = self.stock.ltp*self.quantity
        self.amount = amount
        super(Order, self).save(*args, **kwargs)

