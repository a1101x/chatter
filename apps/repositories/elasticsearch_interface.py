from apps.chat.message import Message
from apps.repositories.interface import ElasticInterfaceBase


class ElasticInterface(ElasticInterfaceBase):
    """
    Implementation of elasticsearch interface.
    """

    def append_message(self, room, user, created, message, status, tags):
        """
        Save message to the elasticsearch index.
        """
        msg = [Message(
            room=room,
            user=user,
            created=created,
            message=message,
            status=status,
            tags=tags
        )]
        print(msg)
        # MessageSaver.save_message.delay(msg)

    def get_messages(self, room, limit):
        """
        Get messages from elastic for selected room.
        """
        pass
