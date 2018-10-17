from django.contrib import admin
from stockmarket.models import Stock,CustomUser,Order
# Register your models here.
admin.site.register(Stock)
admin.site.register(CustomUser)
admin.site.register(Order)