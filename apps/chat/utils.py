from channels.db import database_sync_to_async

from apps.chat.exceptions import ClientError
from apps.chat.models import Room


@database_sync_to_async
def get_room_or_error(room_uuid, user):
    """
    Check user auth, permissions and room existence.
    """
    if not user.is_authenticated:
        raise ClientError('USER_HAS_TO_LOGIN')

    try:
        room = Room.objects.get(pk=room_uuid)
    except Room.DoesNotExist:
        raise ClientError('ROOM_INVALID')

    if room.staff_only and not user.is_staff:
        raise ClientError('ROOM_ACCESS_DENIED')
    
    return room
