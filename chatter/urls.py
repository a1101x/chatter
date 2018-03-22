from envparse import env
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm, password_reset_complete
from django.urls import include, path

ENVIRONMENT_TYPE = env.str('ENVIRONMENT_TYPE', default='development')

api_urlpatterns = [
    path('user/', include('apps.user.urls')),
    path('user/', include('rest_auth.urls')),
    path('location/', include('apps.location.urls')),
    path('phone/', include('apps.phone.urls')),
]

urlpatterns = [
    path('api/v1/', include(api_urlpatterns)),
    path(
        'password-reset/confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'
    ),
    path('password/reset/done/', password_reset_complete, name='password_reset_complete'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if ENVIRONMENT_TYPE == 'development':
    import debug_toolbar
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title='Chatter API')

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('swagger/', schema_view)
    ] + urlpatterns
