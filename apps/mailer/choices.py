from django.utils.translation import gettext_lazy as _

from apps.utils.enumeration import Enumeration

EMAIL_TYPES = Enumeration(
    [
        (100, 'USER_ACTIVATION', _('User activation')),
        (200, 'FORGOT_PASSWORD', _('Forgot password')),
        (300, 'CHANGE_EMAIL', _('Change email')),
    ]
)
