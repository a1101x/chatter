from typing import List, NamedTuple

from django.contrib.auth import get_user_model

from apps.user.serializers import UserSerializer

User = get_user_model()


class Message(NamedTuple):
    room: str
    user: User
    created: str
    message: str
    status: str
    tags: List[str]

    def to_dict(self):
        return {
            'room': self.room,
            'user': UserSerializer(self.user).data,
            'created': self.created,
            'message': self.message,
            'status': self.status,
            'tags': self.tags
        }
