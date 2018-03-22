from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.messenger.choices import SMS_TYPES
from apps.messenger.tasks import send_templated_sms
from apps.user.utils import default_time_expired, generate_pin_code


class Phone(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='phones',
        on_delete=models.CASCADE,
        help_text=_('A user who owns a phone number.')
    )
    phone_number = PhoneNumberField(
        _('Phone number'),
        db_index=True,
        unique=True,
        help_text=_('Phone number.')
    )
    is_verified = models.BooleanField(
        _('Verified'),
        default=False,
        help_text=_('Is phone verified.')
    )

    class Meta:
        verbose_name = _('Phone number')
        verbose_name_plural = _('Phone numbers')

    def __str__(self):
        return '{} - {}'.format(self.user, self.phone_number)


class PhoneVerificationCode(models.Model):
    phone = models.ForeignKey(
        Phone,
        verbose_name=_('Phone'),
        on_delete=models.CASCADE,
        related_name='phone_verification'
    )
    code = models.CharField(
        _('Code'),
        max_length=4,
        default=generate_pin_code,
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
        verbose_name = _('Phone verification code')
        verbose_name_plural = _('Phone verification codes')

    def __str__(self):
        return '{} - {}'.format(self.phone, self.code)


@receiver(post_save, sender=Phone)
def create_verification_code(sender, instance, created, **kwargs):
    if created:
        code = PhoneVerificationCode.objects.create(phone=instance)
        send_templated_sms.delay(
            SMS_TYPES.PHONE_NUMBER_VERIFICATION, str(instance.phone_number), code.code
        )
