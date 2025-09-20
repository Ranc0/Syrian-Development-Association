
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from dashboard.views import serve_media_file
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# إعدادات Swagger للتوثيق التلقائي للـ API
schema_view = get_schema_view(
    openapi.Info(
        title="Syrian Development API",
        default_version='v1',
        description="API لتطبيق الجمعية السورية للتنمية الاجتماعية",
        contact=openapi.Contact(email="dev@syrian-development.org"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    # لوحة الإدارة
    path('admin/', admin.site.urls),

    # واجهات API للتطبيق
    path('api/user/', include('myappG.urls.account')),
    path('api/beneficiaries/', include('myappG.urls.beneficiaries')),
    path('api/medical-aids/', include('myappG.urls.medical_aids')),
    path('api/material-aids/', include('myappG.urls.material_aids')),
    path('api/activities/', include('myappG.urls.activity')),
    path('api/news/', include('myappG.urls.news')),
    path('api/projects/', include('myappG.urls.projects')),
    path('api/feedback/', include('myappG.urls.feedback')),
    path('api/media/<path:path>/', serve_media_file, name='serve_media_file'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('dashboard/', include('dashboard.urls')),

]

# لخدمة الملفات أثناء التطوير فقط
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
