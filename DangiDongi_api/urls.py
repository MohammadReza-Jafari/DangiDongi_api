from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='url helper')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('doc/', schema_view, name='swagger-ui'),
        path('', include('user.urls')),
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)