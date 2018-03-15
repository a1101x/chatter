from django.utils.translation import ugettext as _
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.user.serializers import UserRegistrationSerializer, SendActivationCodeSerializer


class UserRegistrationViewSet(generics.CreateAPIView):
    """
    post:
        Register new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class SendActivationCodeView(generics.CreateAPIView):
    """
    post:
        Send user email with activation code.
    """
    serializer_class = SendActivationCodeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Send user email with activation code,
        if user with this email exists.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'detail': _('Please check your email to activate your account.')
            },
            status=status.HTTP_200_OK
        )
