from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ['date_joined', 'last_login']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = {'is_superuser', 'user_permissions'}

        if not is_superuser:
            disabled_fields |= {
                'is_staff',
                'groups'
            }

        for f in disabled_fields:
            form.base_fields[f].disabled = True

        return form


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
