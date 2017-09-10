from django.contrib import admin
from stockmarket.models import Stock,CustomUser,Buy_Data
# Register your models here.
admin.site.register(Stock)
admin.site.register(CustomUser)
admin.site.register(Buy_Data)