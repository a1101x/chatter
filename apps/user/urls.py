from django.urls import path

from apps.user.views import UserRegistrationViewSet

app_name = 'user'
urlpatterns = [
    path('registration/', UserRegistrationViewSet.as_view()),
]
