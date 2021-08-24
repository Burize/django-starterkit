from ajax_select.fields import AutoCompleteSelectField
from django.contrib import admin

from market.models import Order
from market.models import OrderProduct

from django import forms


class ProductInline(admin.StackedInline):
    model = OrderProduct
    exclude = ['id']
    extra = 1


class OrderForm(forms.ModelForm):
    account = AutoCompleteSelectField(channel='account_channel')


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['number', 'account__email']
    list_display = ['number', 'get_client_name']
    exclude = ['id']

    form = OrderForm

    inlines = [ProductInline]

    @admin.display(description='Client email', ordering='account__email')
    def get_client_name(self, obj):
        return obj.account.email


admin.site.register(Order, OrderAdmin)
