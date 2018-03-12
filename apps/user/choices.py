from django.utils.translation import gettext_lazy as _

from apps.utils.enumeration import Enumeration

GENDER_TYPES = Enumeration(
    [
        (100, 'MALE', _('Male')),
        (200, 'FEMALE', _('Female'))
    ]
)
