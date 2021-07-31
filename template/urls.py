from django.contrib import admin
from django.urls import include
from django.urls import path
from authentication import urls as auth_urls
from market import urls as market_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(auth_urls)),
    path('market/', include(market_urls)),
]
