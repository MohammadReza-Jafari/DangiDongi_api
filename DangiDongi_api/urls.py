from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Dangi Dongi API",
        default_version='1.0.0 v',
        description="Dangi Dongi Api Doc For Frontend Developer",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="chashm78@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url='http://127.0.0.1:8000/api/'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='api-document'),
        path('identity/', include('user.urls')),
        path('wallet/', include('wallet.urls'))
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)