from django.contrib import admin

from authentication.models import Account


class AccountAdmin(admin.ModelAdmin):
    search_fields = ['email']
    readonly_fields = ['id', 'user']
    list_display = ['email']
    list_filter = ['is_verified']


admin.site.register(Account, AccountAdmin)
