from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext as _


class Phone(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='phones',
        on_delete=models.CASCADE,
        help_text=_('A user who owns a phone number.')
    )
    phone_number = models.CharField(
        _('Phone number'),
        max_length=16,
        validators=[RegexValidator(r'^\+\d{9,15}$')],
        db_index=True,
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
