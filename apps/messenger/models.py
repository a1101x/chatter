from django.db import models
from django.utils.translation import ugettext as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.messenger.choices import SMS_TYPES


class SMSTemplate(models.Model):
    """
    SMS model for storing sms text in db. 
    """
    key = models.IntegerField(
        _('Key'),
        choices=SMS_TYPES,
        unique=True,
        db_index=True,
        help_text=_('SMS type.')
    )
    body = models.CharField(
        _('body'),
        max_length=255,
        db_index=True,
        help_text=_('SMS body.')
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        db_index=True,
        help_text=_('Template creation date.')
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        db_index=True,
        help_text=_('Template update date.')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Is template active.')
    )

    class Meta:
        verbose_name = _('SMS template')
        verbose_name_plural = _('SMS templates')

    def __str__(self):
        return '{} - {}'.format(self.key, self.body)
