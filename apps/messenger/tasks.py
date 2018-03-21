from apps.messenger.models import SMSTemplate
from chatter.celery import app as celery_app

from apps.messenger.interface import TwilioInterface

twilio = TwilioInterface()


@celery_app.task(name='messenger.send_templated_sms', time_limit=30)
def send_templated_sms(key, recipient, body=None):
    """
    Send email with template.
    """
    try:
        sms = SMSTemplate.objects.get(key=key, is_active=True)

        if body:
            text = sms.body.format(*body)
            twilio.create(to=recipient, body=text)
        else:
            twilio.create(to=recipient, body=sms.body)
    except (SMSTemplate.DoesNotExist, KeyError) as e:
        return str(e)


@celery_app.task(name='messenger.send_simple_sms', time_limit=30)
def send_simple_sms(body, recipient):
    """
    Send simple sms, do not user template from db.
    """
    twilio.create(to=recipient, body=body)
