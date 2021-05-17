from django.contrib import admin

# Register your models here.
from .models import Customer,Products,Order,Tags,Downline,OrderItem,Checkout
admin.site.register(Customer),
admin.site.register(Products),
admin.site.register(Order),
admin.site.register(Tags),
admin.site.register(OrderItem),
admin.site.register(Downline),
admin.site.register(Checkout)


