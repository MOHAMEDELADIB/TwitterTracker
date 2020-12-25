from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from accounts.views import ChangeTwitterView
from main.views import  ChangeLanguageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',  ChangeTwitterView.as_view(), name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)