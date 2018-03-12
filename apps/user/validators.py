from django.contrib.auth.validators import UnicodeUsernameValidator
from django.forms import ValidationError
from django.utils.translation import ugettext as _

username_validator = UnicodeUsernameValidator()


def validate_profile_pic(obj):
    """
    Checking the avatar size.
    """
    size = obj.file.size
    limit = 2.0

    if size > limit * 1024 * 1024:
        raise ValidationError(_('The image should be less than 2 MB.'))
