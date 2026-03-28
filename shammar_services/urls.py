"""
URL configuration for shammar_services project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mabipint.urls')),
    # PWA: Servir le service worker à la racine
    path('service-worker.js', TemplateView.as_view(template_name="service-worker.js", content_type='application/javascript'), name='service-worker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
