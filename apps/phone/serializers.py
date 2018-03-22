from django.utils.translation import ugettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from apps.phone.models import Phone


class PhoneListSerializer(serializers.ModelSerializer):
    """
    Serializer for Phone model.
    """
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(
                queryset=Phone.objects.all(),
                message=_('Someone is already using this phone number.')
            )
        ],
        error_messages={
            'invalid': _('Phone number must starts with + and contain only numbers.')
        }
    )

    class Meta:
        model = Phone
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True,
                'default': serializers.CurrentUserDefault()
            },
            'is_verified': {'read_only': True}
        }


class PhoneDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for phone model.
    """
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(
                queryset=Phone.objects.all(),
                message=_('Someone is already using this phone number.')
            )
        ],
        error_messages={
            'invalid': _('Phone number must starts with + and contain only numbers.')
        }
    )

    class Meta:
        model = Phone
        fields = ('phone_number',)


class PhoneVerificationSerializer(serializers.Serializer):
    """
    Serializer for phone verification.
    """
    phone_number = PhoneNumberField(
        error_messages={
            'invalid': _('Phone number must starts with + and contain only numbers.')
        }
    )
    user = serializers.CharField(default=serializers.CurrentUserDefault())
    code = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        fields = '__all__'

    def validate_phone_number(self, value):
        """
        Check if phone exists and belongs to the current user.
        Returns user or None.
        """
        phone = None

        try:
            phone = Phone.objects.get(phone_number=value)
        except Phone.DoesNotExist:
            raise serializers.ValidationError(
                {
                    'phone': _('This phone number is not in the database.')
                },
                code=status.HTTP_404_NOT_FOUND
            )

        return value

    def validation(self, data):
        """
        Verify phone number if it is user 
        """
        return data