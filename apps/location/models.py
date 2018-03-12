from django.conf import settings
from django.db.models import Manager as GeoManager
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField


class Zipcode(models.Model):
    code = models.CharField(
        _('Zipcode'),
        max_length=5,
        help_text=_('Zipcode.')
    )
    poly = models.PolygonField(
        _('Poly'),
        help_text=_('Poly.')
    )

    objects = GeoManager()

    class Meta:
        verbose_name = _('Zipcode')
        verbose_name_plural = _('Zipcodes')

    def __str__(self):
        return '{}'.format(self.code)


class Location(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='locations',
        on_delete=models.CASCADE,
        help_text=_('A user who have this location.')
    )
    street = models.CharField(
        _('Street'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Street.')
    )
    city = models.CharField(
        _('City'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('City.')
    )
    state = models.CharField(
        _('State'),
        max_length=2,
        blank=True,
        null=True,
        help_text=_('State.')
    )
    zipcode = models.ForeignKey(
        Zipcode,
        verbose_name=_('Zipcode'),
        related_name='addresses',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_('Zipcode.')
    )
    country = CountryField(
        multiple=True,
        blank_label=_('(Select country)'),
        blank=True, default='',
        db_index=True
    )
    point = models.PointField(
        null=True,
        spatial_index=True,
        geography=True
    )

    objects = GeoManager()

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return '{} - {}, {}, {}'.format(self.user, self.country, self.city, self.street)
