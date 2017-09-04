from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField,ArrayField
# Create your models here.

class Stock(models.Model):

    stock_name = models.CharField(max_length=10)
    buy_price = models.FloatField(default=0)
    current_price = models.FloatField(default=0)
    #transact_counter = models.IntegerField(default=0)
    buy_quantity = models.IntegerField(default=0)
    #sell_quantity = models.IntegerField(default=0)
    #buy_data = ArrayField(JSONField(), size=10000,default={'buy_price':0,'quantity':0})
    #average_buy_price = models.FloatField(default=0)
    def __str__(self):
        return self.stock_name

class CustomUser(AbstractUser):

    stocks = models.ManyToManyField(Stock)
    total_fund = models.FloatField(default=500000.0)
    def __str__(self):
        return self.username

