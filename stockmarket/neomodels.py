from neo4django.db import models
from properties import FloatProperty

class User(models.NodeModel):

    username = models.StringProperty()
    email = models.EmailProperty()
    fund_balance = FloatProperty()

class Stock(models.NodeModel):

    name = models.StringProperty()
    ltp = FloatProperty()

class Order(models.NodeModel):

    trader = models.Relationship(User, rel_type='owns', related_name='orders')
    _type = models.StringProperty(max_length=4)
    quantity = models.IntegerProperty()
    amount = FloatProperty()

