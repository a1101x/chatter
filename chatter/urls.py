from envparse import env
from django.contrib import admin
from django.urls import include, path

ENVIRONMENT_TYPE = env.str('ENVIRONMENT_TYPE', default='development')

api_urlpatterns = [
    path('user/', include('apps.user.urls')),
    path('user/', include('rest_auth.urls')),
]

urlpatterns = [
    path('api/v1/', include(api_urlpatterns)),
    path('admin/', admin.site.urls),
]

if ENVIRONMENT_TYPE == 'development':
    import debug_toolbar
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title='Chatter API')

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('swagger/', schema_view)
    ] + urlpatterns
