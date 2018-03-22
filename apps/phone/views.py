from django.utils.translation import ugettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.phone.models import Phone
from apps.phone.permissions import IsPhoneNumberOwnerOrReadOnly
from apps.phone.serializers import PhoneDetailSerializer, PhoneListSerializer, PhoneVerifySerializer, SendVerificationCodeSerializer


class PhoneListView(generics.ListCreateAPIView):
    """
    get:
        Get list of user phone numbers.

    post:
        Create new phone number.
    """
    serializer_class = PhoneListSerializer
    queryset = Phone.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('id', 'user', 'is_verified')
    ordering_fields = ('id', 'user', 'phone_number', 'is_verified')
    search_fields = ('user__email', 'phone_number')
    ordering = ('id',)


class PhoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Get user phone detail.

    put:
        Update user phone.
        Availiable only for phone owners.

    patch:
        Update user phone.
        Availiable only for phone owners.

    delete:
        Delete phone.
        Availiable only for phone owners.
    """
    serializer_class = PhoneDetailSerializer
    permission_classes = (IsPhoneNumberOwnerOrReadOnly,)
    queryset = Phone.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PhoneListSerializer

        return PhoneDetailSerializer


class SendPhoneVerificationCodeView(generics.CreateAPIView):
    """
    post:
        Send user sms with verification code.
    """
    serializer_class = SendVerificationCodeSerializer


class PhoneVerificationView(generics.GenericAPIView):
    """
    post:
        Verify user phone number.
    """
    serializer_class = PhoneVerifySerializer
    queryset = Phone.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Check serializer and activate user if serializer is valid.

        post params:
            phone_number, code
        return:
            success status, status code, additional data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'detail': _('Congratulations! Your phone number has been verified.')
            },
            status=status.HTTP_200_OK
        )
