from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.user.serializers import UserRegistrationSerializer


class UserRegistrationViewSet(generics.CreateAPIView):
    """
    post:
        Register new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
