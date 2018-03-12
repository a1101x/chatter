from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from apps.mailer.choices import EMAIL_TYPES
from apps.mailer.tasks import send_templated_email
from apps.phone.models import Phone
from apps.user.utils import generate_pin_code

User = get_user_model()


class JWTUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.
    """
    class Meta:
        model = User
        fields = ('pk', 'username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    # Phone
    phone_number = serializers.RegexField(
        regex=r'^\d{9,15}$', required=False,
        validators=[
            UniqueValidator(
                queryset=Phone.objects.all(),
                message=_('The phone number already exists.')
            )
        ],
        error_messages={
            'invalid': _('Phone number must contain only numbers.')
        }
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'birthday', 'username', 'gender', 'email', 'password', 'photo',
            # Phone model
            'phone_number'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'validators': [
                    RegexValidator(
                        regex=r'^[a-zA-Z0-9()_^%$#!~@-]{8,32}$',
                        message='The password must be 8 to 32 characters in length.'
                                'Can contain letters, numbers and special characters (()_^%$#!~@-).'
                    )
                ]
            }
        }

    def validate_birthday(self, value):
        """
        Min year = 1930.
        """
        if value:
            today = timezone.now().today()

            if value.year < 1930 or value.year > today.year:
                raise serializers.ValidationError(
                    _('Please, select a year higher than 1930 and lower than current year.'),
                    code=status.HTTP_400_BAD_REQUEST
                )

        return value

    def create(self, validated_data):
        """
        Create user and Phone if it needed.
        """
        phone = validated_data.pop('phone_number', None)
        user = User(**validated_data)
        user.is_active = False
        user.save()

        if phone is not None:
            Phone.objects.create(user=user, phone_number=phone)

        send_templated_email.delay(
            key=EMAIL_TYPES.USER_ACTIVATION,
            recipient_list=validated_data.get('email'),
            context={'code': generate_pin_code()}
        )
        return user
