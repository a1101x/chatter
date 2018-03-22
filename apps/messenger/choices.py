from django.utils.translation import gettext_lazy as _

from apps.utils.enumeration import Enumeration

SMS_TYPES = Enumeration(
    [
        (100, 'PHONE_NUMBER_VERIFICATION', _('Phone number verification')),
        (200, 'FORGOT_USERNAME_EMAIL', _('Forgot username/email'))
    ]
)
