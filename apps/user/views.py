from django.utils.translation import ugettext as _
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.user.serializers import SendActivationCodeSerializer, UserActivationSerializer, UserRegistrationSerializer


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


class UserActivationView(generics.GenericAPIView):
    """
    post:
        Activate user with activation code.
    """
    serializer_class = UserActivationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Check serializer and activate user if serializer is valid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'detail': _('Congratulations! Your account has been activated.')
            },
            status=status.HTTP_200_OK
        )
