import uuid

from django.db import models
from django.utils.translation import ugettext as _


class Room(models.Model):
    id = models.UUIDField(
        _('UUID Primary key'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    staff_only = models.BooleanField(
        _('Staff only'),
        default=False,
        help_text=_('This room can be available only for staff users.')
    )

    def __str__(self):
        return str(self.id)

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return 'room-{}'.format(self.id)
