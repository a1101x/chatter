from django.urls import path

from apps.phone.views import PhoneDetailView, PhoneListView, PhoneVerificationView, SendPhoneVerificationCodeView

app_name = 'phone'
urlpatterns = [
    path('list/', PhoneListView.as_view()),
    path('<int:pk>/', PhoneDetailView.as_view()),
    path('send-verification-code/', SendPhoneVerificationCodeView.as_view()),
    path('verify/', PhoneVerificationView.as_view()),
]
