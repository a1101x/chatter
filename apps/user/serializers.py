from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from apps.mailer.choices import EMAIL_TYPES
from apps.mailer.tasks import send_templated_email
from apps.phone.models import Phone
from apps.user.models import UserActivationCode
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
        regex=r'^\+\d{9,15}$', required=False,
        validators=[
            UniqueValidator(
                queryset=Phone.objects.all(),
                message=_('The phone number already exists.')
            )
        ],
        error_messages={
            'invalid': _('Phone number must starts with + and contain only numbers.')
        },
        write_only=True
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
        
        pin_code = generate_pin_code()
        code = UserActivationCode(user=user, code=pin_code)
        code.save()
        send_templated_email.delay(
            key=EMAIL_TYPES.USER_ACTIVATION,
            recipient_list=validated_data.get('email'),
            context={'code': pin_code}
        )
        return user


class ActivationCodeSerializer(serializers.ModelSerializer):
    """
    Base serializer for user activation.
    """
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = UserActivationCode
        fields = ('email',)

    def validate_email(self, value):
        """
        Checks whether the user exists and is user inactive.
        """
        try:
            self.user = User.objects.get(email__iexact=value)

            if self.user.is_active:
                raise serializers.ValidationError(
                    _('User account is already activated.'),
                    code=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _('User with this email does not exist.'),
                code=status.HTTP_400_BAD_REQUEST
            )

        return value


class SendActivationCodeSerializer(ActivationCodeSerializer):
    """
    Send user activation code.
    """
    def create(self, validated_data):
        """
        Creates a model in db after email validation.
        """
        pin_code = generate_pin_code()
        send_templated_email.delay(
            key=EMAIL_TYPES.USER_ACTIVATION,
            recipient_list=validated_data.get('email'),
            context={'code': pin_code}
        )
        user_activation_code = UserActivationCode(
            user=self.user,
            code=pin_code
        )
        user_activation_code.save()
        return user_activation_code
