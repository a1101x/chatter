from django.urls import path

from apps.user.views import (
    ForgotUsernameEmailView, SendActivationCodeView, UserActivationView, UserDetailView, UserListView,
    UserRegistrationViewSet
)

app_name = 'user'
urlpatterns = [
    path('signup/', UserRegistrationViewSet.as_view()),
    path('send-activation-code/', SendActivationCodeView.as_view()),
    path('user-activation/', UserActivationView.as_view()),
    path('forgot-username-email/', ForgotUsernameEmailView.as_view()),
    path('list/', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
]
