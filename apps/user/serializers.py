from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from apps.mailer.choices import EMAIL_TYPES
from apps.mailer.tasks import send_templated_email
from apps.messenger.choices import SMS_TYPES
from apps.messenger.tasks import send_templated_sms
from apps.phone.models import Phone
from apps.user.models import UserActivationCode

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
            phone = Phone.objects.create(user=user, phone_number=phone)
        
        return user


class ActivationCodeSerializer(serializers.ModelSerializer):
    """
    Base serializer for user activation.
    """
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = UserActivationCode

    def validate_email(self, value):
        """
        Checks whether the user exists and is user inactive.
        """
        try:
            self.user = User.objects.only('email', 'is_active').get(email__iexact=value)

            if self.user.is_active:
                raise serializers.ValidationError(
                    _('User account is already activated.'),
                    code=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _('User with this email does not exist.'),
                code=status.HTTP_404_NOT_FOUND
            )

        return value


class SendActivationCodeSerializer(ActivationCodeSerializer):
    """
    Send activation code to a user.
    """
    class Meta(ActivationCodeSerializer.Meta):
        model = UserActivationCode
        fields = ('email', 'user', 'time_expired')
        extra_kwargs = {
            'user': {'read_only': True},
            'time_expired': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Creates an activation code model in db after email validation.
        """
        code = UserActivationCode.objects.create(user=self.user)
        send_templated_email.delay(
            key=EMAIL_TYPES.USER_ACTIVATION,
            recipient_list=validated_data.get('email'),
            context={'code': code.code}
        )
        return code


class UserActivationSerializer(ActivationCodeSerializer):
    """
    User activation using cactivation code.
    """
    class Meta(ActivationCodeSerializer.Meta):
        fields = ('email', 'user', 'code')
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate_code(self, value):
        """
        Pin code validation.
        """
        try:
            code = UserActivationCode.objects.filter(user=self.user).latest('created')

            if code.code == value:
                if code.time_expired < timezone.now():
                    raise serializers.ValidationError(
                        _('The activation code is already expired.'),
                        code=status.HTTP_400_BAD_REQUEST
                    )
            else:
                raise serializers.ValidationError(
                    _('The activation code is not valid for this user.'),
                    code=status.HTTP_400_BAD_REQUEST
                )
        except UserActivationCode.DoesNotExist:
            raise serializers.ValidationError(
                _('There are no any activation codes for this user.'),
                code=status.HTTP_404_NOT_FOUND
            )
        
        return value

    def validate(self, data):
        """
        Make user active.
        """
        self.user.is_active = True
        self.user.save()
        return data


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_password(self, user, password):
        """
        Check user password.
        """
        if not user.check_password(password):
            raise serializers.ValidationError(
                {
                    'password': _('This is not a valid password for this user.')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

    def _validate_username_email(self, username, email, password):
        """
        Check if user exist and try to authenticate with provided credentials.
        Returns user or None.
        """
        user = None

        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        'email': _('User with this email does not exist.')
                    },
                    code=status.HTTP_404_NOT_FOUND
                )

            self._validate_password(user, password)
            user = authenticate(email=email, password=password)
        elif username and password:
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        'username': _('User with this username does not exist.')
                    },
                    code=status.HTTP_404_NOT_FOUND
                )

            self._validate_password(user, password)
            user = authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError(
                {
                    'username': _('Must include either "username" or "email".'),
                    'email': _('Must include either "username" or "email".'),
                    'password': _('This field is required.')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        return user

    def validate(self, data):
        """
        Check if the user is activated.
        """
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        user = self._validate_username_email(username, email, password)

        if user:
            if not user.is_active:
                raise serializers.ValidationError(
                    {
                        'user': _('This account is currently inactive.')
                    },
                    code=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise serializers.ValidationError(
                {
                    'user': _('Unable to log in with provided credentials.')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)

                if not email_address.verified:
                    raise serializers.ValidationError(
                        {
                            'email': _('E-mail is not verified.')
                        },
                        code=status.HTTP_400_BAD_REQUEST
                    )

        data['user'] = user
        return data


class ForgotUsernameEmailSerializer(serializers.Serializer):
    """
    Sends username and email on user phone number.
    """
    phone_number = PhoneNumberField(
        error_messages={
            'invalid': _('Phone number must starts with + and contain only numbers.')
        }
    )

    class Meta:
        fields = '__all__'

    def validate_phone_number(self, value):
        """
        Check if the phone number is in the db.
        """
        try:
            self.phone = Phone.objects.select_related('user').only(
                'user__username', 'user__email', 'phone_number', 'is_verified'
            ).get(phone_number=value)

            if not self.phone.is_verified:
                raise serializers.ValidationError(
                    _('Phone number does not verified.'),
                    code=status.HTTP_400_BAD_REQUEST
                )
        except Phone.DoesNotExist:
            raise serializers.ValidationError(
                _('Phone number does not exist.'),
                code=status.HTTP_404_NOT_FOUND
            )
        
        return value

    def validate(self, data):
        """
        Send sms with username and email.
        """
        body = (self.phone.user.username, self.phone.user.email)
        send_templated_sms.delay(
            SMS_TYPES.FORGOT_USERNAME_EMAIL, str(self.phone.phone_number), body
        )
        return data
