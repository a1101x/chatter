from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from apps.mailer.choices import EMAIL_TYPES
from apps.mailer.tasks import send_templated_email
from apps.user.choices import GENDER_TYPES
from apps.user.utils import default_time_expired, generate_pin_code
from apps.user.validators import username_validator, validate_profile_pic


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **kwargs):
        """
        Set kwargs for simple user.
        """
        for field in ('is_staff', 'is_superuser', 'is_active'):
            kwargs.setdefault(field, False)

        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        """
        Set kwargs for superuser.
        """
        for field in ('is_staff', 'is_superuser', 'is_active'):
            if kwargs.setdefault(field, True) is not True:
                raise ValueError('Superuser must have {}=True'.format(field))

        return self._create_user(username, email, password, **kwargs)


class User(AbstractUser):
    first_name = models.CharField(
        _('First name'),
        max_length=120,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('First name.')
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=120,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Last name.')
    )
    birthday = models.DateField(
        _('Birthday'),
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Date of birth.')
    )
    username = models.CharField(
        _('Username'),
        max_length=32,
        validators=[username_validator],
        unique=True,
        db_index=True,
        help_text=_('32 characters or fewer. Letters, digits and @/./+/-/_.'),
        error_messages={
            'unique': _('A user with that username already exists.')
        }
    )
    gender = models.PositiveSmallIntegerField(
        _('Gender'),
        choices=GENDER_TYPES,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Gender (100 - Male, 200 - Female).')
    )
    email = models.EmailField(
        _('E-mail address'),
        unique=True,
        db_index=True,
        help_text=_('User email.')
    )
    photo = models.ImageField(
        _('Photo'),
        upload_to='users',
        validators=[validate_profile_pic],
        blank=True,
        null=True
    )

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return '{}'.format(self.username)


class UserActivationCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='code'
    )
    code = models.CharField(
        _('Code'),
        default=generate_pin_code,
        max_length=4,
        db_index=True
    )
    time_expired = models.DateTimeField(
        _('Time expired'),
        default=default_time_expired,
        db_index=True
    )
    created = models.DateTimeField(
        _('Creation time'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = _('User activation code')
        verbose_name_plural = _('User activation codes')

    def __str__(self):
        return '{} - {}'.format(self.user, self.code)


class ChangeEmailCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='email_code'
    )
    code = models.CharField(
        _('Code'),
        default=generate_pin_code,
        max_length=4,
        db_index=True
    )
    new_email = models.EmailField(
        _('New email'),
        max_length=254,
        blank=True,
        null=True,
        db_index=True
    )
    time_expired = models.DateTimeField(
        _('Time expired'),
        default=default_time_expired,
        db_index=True
    )
    created = models.DateTimeField(
        _('Creation time'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = _('Change email code')
        verbose_name_plural = _('Change email codes')

    def __str__(self):
        return '{} - {}'.format(self.user, self.code)


@receiver(post_save, sender=User)
def create_activation_code(sender, instance, created, **kwargs):
    if created:
        code = UserActivationCode.objects.create(user=instance)
        send_templated_email.delay(
            key=EMAIL_TYPES.USER_ACTIVATION,
            recipient_list=instance.email,
            context={'code': code.code}
        )
