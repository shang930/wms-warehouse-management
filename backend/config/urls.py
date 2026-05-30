"""Root URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls.auth', namespace='auth')),
    path('api/v1/users/', include('apps.users.urls.users', namespace='users')),
    path('api/v1/goods/', include('apps.goods.urls', namespace='goods')),
    path('api/v1/warehouses/', include('apps.warehouse.urls', namespace='warehouses')),
    path('api/v1/suppliers/', include('apps.supplier.urls', namespace='suppliers')),
    path('api/v1/customers/', include('apps.customer.urls', namespace='customers')),
    path('api/v1/stock/', include('apps.stock.urls', namespace='stock')),
    path('api/v1/asn/', include('apps.asn.urls', namespace='asn')),
    path('api/v1/dn/', include('apps.dn.urls', namespace='dn')),
    path('api/v1/cyclecount/', include('apps.cyclecount.urls', namespace='cyclecount')),
    path('api/v1/assets/', include('apps.capital.urls', namespace='capital')),
    path('api/v1/reports/', include('apps.report.urls', namespace='reports')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
