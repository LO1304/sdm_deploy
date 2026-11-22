import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse


def service_worker_view(request):
    """Sert le vrai Service Worker hors-ligne complet à la racine /sw.js avec portée globale /."""
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    with open(sw_path, 'r', encoding='utf-8') as f:
        content = f.read()
    resp = HttpResponse(content, content_type='application/javascript; charset=utf-8')
    resp['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp['Service-Worker-Allowed'] = '/'
    return resp


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bibliotheque.api_urls')),
    path('', include('bibliotheque.urls')),
    path('sw.js', service_worker_view, name='sw.js'),
]

# Service des fichiers MEDIA et STATIC pour la production sur Render
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]