from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from moudles.user import views as u_views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()



urlpatterns = [
    path('demo/api/', include(router.urls)),
    path('demo/api/projects/', include('moudles.projects.url')),
    path('demo/admin/', admin.site.urls),
    path('demo/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('demo/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('demo/api/api-token-auth/', u_views.ObtainExpiringAuthToken.as_view(), name='api_token_auth'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]