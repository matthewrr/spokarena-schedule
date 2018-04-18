from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^sms/', include('sms.urls')),
    path('admin/', admin.site.urls),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)