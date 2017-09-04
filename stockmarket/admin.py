from django.contrib import admin
from stockmarket.models import Stock,CustomUser
# Register your models here.
admin.site.register(Stock)
admin.site.register(CustomUser)