from django.conf.urls import re_path
from django.contrib import admin
from django.urls import include
from django.urls import path
from authentication import urls as auth_urls
from market import urls as market_urls
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    re_path(r'^ajax_select/', include(ajax_select_urls)),
    path('admin/', admin.site.urls),
    path('', include(auth_urls)),
    path('market/', include(market_urls)),
]

handler404 = 'template.api.exception_handler.handle_not_found_path'
