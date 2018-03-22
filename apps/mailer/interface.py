import requests
from django.conf import settings

API_SETTINGS = {
    'api': settings.MAILGUN_API_KEY,
    'base_url': settings.MAILGUN_BASE_URL
}


class MailgunInterface(object):
    """
    Parent class for using mailgun, used by other classes (in future?).
    """
    def __init__(self):
        """
        Creates basic configuration dictionary.
        """
        self.auth = ('api', API_SETTINGS['api'])
        self.base_url = API_SETTINGS['base_url']

    def send(self, from_=None, to_=None, subject=None, text=None, html=None):
        """
        Primary send API method.
        """
        response = requests.post(
            self.base_url,
            auth=self.auth,
            data={
                'from': from_,
                'to': to_,
                'subject': subject,
                'text': text,
                'html': html
            }
        )
        return response
