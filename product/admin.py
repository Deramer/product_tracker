from django.contrib import admin

from product.models import Product, UserProduct

@admin.register(Product, UserProduct)
class BaseAdmin(admin.ModelAdmin):
    pass
