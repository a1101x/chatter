from django.utils import timezone
from django.utils.translation import ugettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from apps.messenger.choices import SMS_TYPES
from apps.messenger.tasks import send_templated_sms
from apps.phone.models import Phone, PhoneVerificationCode


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

    def update(self, instance, validated_data):
        """
        Set phone number as unverified on at update.
        """
        instance.phone_number = validated_data.get('phone_number')
        instance.is_verified = False
        instance.save()
        return instance


class PhoneVerificationCodeSerializer(serializers.ModelSerializer):
    """
    Base serializer for phone verification.
    """
    phone_number = PhoneNumberField(
        write_only=True,
        error_messages={
            'invalid': _('Phone number must starts with + and contain only numbers.')
        }
    )

    class Meta:
        model = PhoneVerificationCode

    def validate_phone_number(self, value):
        """
        Check if phone exists and not verified.
        """
        try:
            self.phone = Phone.objects.only(
                'user__id', 'phone_number', 'is_verified'
            ).select_related('user').get(phone_number=value)

            if self.phone.is_verified:
                raise serializers.ValidationError(
                _('This phone number is already verified.'),
                code=status.HTTP_400_BAD_REQUEST
            )
        except Phone.DoesNotExist:
            raise serializers.ValidationError(
                _('This phone number is not in the database.'),
                code=status.HTTP_404_NOT_FOUND
            )

        return value


class SendVerificationCodeSerializer(PhoneVerificationCodeSerializer):
    """
    Send verification code on the phone number.
    """
    class Meta(PhoneVerificationCodeSerializer.Meta):
        fields = ('phone_number',)

    def create(self, validated_data):
        """
        Creates an verification code model in db after phone number validation.
        """
        code = PhoneVerificationCode.objects.create(phone=self.phone)
        send_templated_sms.delay(
            key=SMS_TYPES.PHONE_NUMBER_VERIFICATION,
            recipient=str(validated_data.get('phone_number')),
            body=(code.code,)
        )
        return code


class PhoneVerifySerializer(PhoneVerificationCodeSerializer):
    """
    Serializer for phone verification.
    """
    user = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta(PhoneVerificationCodeSerializer.Meta):
        fields = ('phone_number', 'user', 'code')
        extra_kwargs = {
            'code': {'required': True},
            'phone_number': {'required': True}
        }

    def validate_code(self, value):
        """
        Pin code validation.
        """
        try:
            code = PhoneVerificationCode.objects.filter(phone=self.phone).latest('created')

            if code.code == value:
                if code.time_expired < timezone.now():
                    raise serializers.ValidationError(
                        _('The verification code is already expired.'),
                        code=status.HTTP_400_BAD_REQUEST
                    )
            else:
                raise serializers.ValidationError(
                    _('The verification code is not valid for this phone number.'),
                    code=status.HTTP_400_BAD_REQUEST
                )
        except PhoneVerificationCode.DoesNotExist:
            raise serializers.ValidationError(
                _('There are no any verification codes for this phone number.'),
                code=status.HTTP_404_NOT_FOUND
            )
        
        return value

    def validate(self, data):
        """
        Verify phone number.
        """
        if self.phone.user != data.get('user'):
            raise serializers.ValidationError(
                {
                    'phone_number': _('Only phone number owner can verify phone.')
                },
                code=status.HTTP_400_BAD_REQUEST
            )
        
        self.phone.is_verified = True
        self.phone.save()
        return data
