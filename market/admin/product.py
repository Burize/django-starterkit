from django.contrib import admin

from market.models import Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    exclude = ['id']


admin.site.register(Product, ProductAdmin)
