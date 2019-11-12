from django.contrib import admin
from .models import Product,SellProduct
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','create_time']
    #search_fields = ['classes__name','teacher__teacher__username','classes__major__grade']
    #ordering = ['-semester','classes__major__grade']

@admin.register(SellProduct)
class SellProductAdmin(admin.ModelAdmin):
    list_display = ['belong','product','price']