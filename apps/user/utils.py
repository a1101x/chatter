import string
from datetime import timedelta
from random import choice, randrange, shuffle

from django.conf import settings
from django.utils import timezone


def generate_pin_code():
    """
    Generate 4 digit pin-code.
    """
    secret = list(randrange(0, 9) for _ in range(4))
    shuffle(secret)
    return ''.join(map(str, secret))


def generate_password():
    """
    Generate random alphanumeric password.
    """
    secret = ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(9))
    return secret


def default_time_expired():
    """
    Get activation code expiration time.
    """
    time = timezone.now() + timedelta(minutes=settings.ACTIVATION_CODE_LIFETIME)
    return time
