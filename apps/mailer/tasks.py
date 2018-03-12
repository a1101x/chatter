import requests
from django.conf import settings
from django.core.mail import send_mail

from apps.mailer.models import EmailTemplate
from chatter.celery import app as celery_app


@celery_app.task(name='mailer.send_templated_email', time_limit=30)
def send_templated_email(key, recipient_list, context={}, template_name=None, from_email=None):
    """
    Send email with html template.
    """
    try:
        mail = EmailTemplate.objects.get(key=key, is_active=True)

        if from_email is None:
            from_email = settings.EMAIL_TEMPLATE_DEFAULTS['FROM_EMAIL']

        email = mail.render(context, template_name)
        requests.post(
            settings.MAILGUN_BASE_URL,
            auth=('api', settings.MAILGUN_API_KEY),
            data={
                'from': from_email,
                'to': recipient_list,
                'subject': email['subject'],
                'text': email['message'],
                'html': email['html_message'],
            }
        )
    except (EmailTemplate.DoesNotExist, KeyError):
        pass


@celery_app.task(name='mailer.send_simple_mail', time_limit=30)
def send_simple_mail(subject, body, from_email, to_email):
    """
    Send simple email, only text.
    """
    requests.post(
        settings.MAILGUN_BASE_URL,
        auth=('api', settings.MAILGUN_API_KEY),
        data={
            'from': from_email,
            'to': to_email,
            'subject': subject,
            'text': body
        }
    )
