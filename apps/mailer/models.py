import html2text
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template import Context, Template, loader
from django.utils.translation import ugettext as _
from premailer import transform

from apps.mailer.choices import EMAIL_TYPES


class EmailTemplate(models.Model):
    """
    Email model for storing template in database.
    """
    key = models.IntegerField(
        _('Key'),
        choices=EMAIL_TYPES,
        unique=True,
        db_index=True,
        help_text=_('Email type.')
    )
    subject = models.CharField(
        _('Subject'),
        max_length=255,
        db_index=True,
        help_text=_('Email subject.')
    )
    title = models.CharField(
        _('Title'),
        max_length=255,
        db_index=True,
        help_text=_('Email title.')
    )
    body = models.TextField(
        _('Content'),
        db_index=True,
        help_text=_('Email body.')
    )
    button_label = models.CharField(
        _('Button label'),
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_('Template button label.')
    )
    button_link = models.CharField(
        _('Button Link'),
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_('Template button link.')
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        db_index=True,
        help_text=_('Template creation date.')
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        db_index=True,
        help_text=_('Template update date.')
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Is template active.')
    )

    class Meta:
        verbose_name = _('E-mail template')
        verbose_name_plural = _('E-mail templates')

    def __str__(self):
        return '{} - {}'.format(self.key, self.subject)

    def render(self, context, template_name=None):
        """
        Render template.
        """
        if template_name is None:
            try:
                template_name = settings.EMAIL_TEMPLATE_DEFAULTS['TEMPLATE_NAME']
            except KeyError:
                raise ImproperlyConfigured(
                    _('Need to configure TEMPLATE_NAME.')
                )

        try:
            context_default = settings.EMAIL_TEMPLATE_DEFAULTS['CONTEXT']
        except KeyError:
            pass

        context_default.update(context)
        context_default.update({
            'title': Template(self.title).render(Context(context_default)),
            'button_label': Template(self.button_label).render(Context(context_default)),
            'button_link': Template(self.button_link).render(Context(context_default)),
            'body': Template(self.body).render(Context(context_default)),
        })
        html = loader.render_to_string(template_name, context_default)

        try:
            base_url = settings.EMAIL_TEMPLATE_DEFAULTS['BASE_URL']
        except KeyError:
            raise ImproperlyConfigured(
                _('Need to configure BASE_URL.')
            )

        html = transform(html, base_url=base_url)
        h = html2text.HTML2Text()
        h.ignore_images = True
        h.ignore_tables = True
        text = h.handle(html)
        response = {
            'subject': Template(self.subject).render(Context(context_default)),
            'message': text,
            'html_message': html
        }
        return response
