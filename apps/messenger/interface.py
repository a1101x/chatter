import abc

from django.conf import settings
from twilio.rest import Client

API_SETTINGS = {
    'account_sid': settings.TWILIO_ACCOUNT_SID,
    'auth_token': settings.TWILIO_AUTH_TOKEN,
    'from_': settings.TWILIO_NUMBER
}


class TwilioInterfaceBase(abc.ABC):
    """
    Base Twilio interface.
    """
    def __init__(self):
        """
        Creates basic configuration dictionary.
        """
        self.client = Client(API_SETTINGS['account_sid'], API_SETTINGS['auth_token'])

    def create(self, to=None, from_=None, body=None):
        """
        Primary send sms method.
        Need to implement in child class.
        """
        raise NotImplementedError


class TwilioInterface(TwilioInterfaceBase):
    """
    Parent class for using twilio, used by other classes (in future?).
    """
    def create(self, to=None, from_=None, body=None):
        """
        Primary send sms method.
        """
        response = self.client.messages.create(
            to, from_ if from_ else API_SETTINGS['from_'], body
        )
        return response
