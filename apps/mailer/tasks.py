from django.conf import settings

from apps.mailer.interface import MailgunInterface
from apps.mailer.models import EmailTemplate
from chatter.celery import app as celery_app

mailgun = MailgunInterface()


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
        mailgun.send(
            from_email, recipient_list, email['subject'], email['message'], email['html_message']
        )
    except (EmailTemplate.DoesNotExist, KeyError) as e:
        return str(e)


@celery_app.task(name='mailer.send_simple_mail', time_limit=30)
def send_simple_mail(subject, body, from_email, to_email):
    """
    Send simple email, only text.
    """
    mailgun.send(from_email, to_email, subject, body)
