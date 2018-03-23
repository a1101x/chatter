from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from apps.chat.exceptions import ClientError
from apps.chat.utils import get_room_or_error


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Chat consumer that handles websocket connections for chat clients.
    """

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.accept()

        self.rooms = set()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        command = content.get('command', None)
        
        try:
            if command == 'join':
                await self.join_room(content['room'])
            elif command == 'leave':
                await self.leave_room(content['room'])
            elif command == 'send':
                await self.send_room(content['room'], content['message'])
        except ClientError as e:
            await self.send_json({'error': e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        for room_uuid in list(self.rooms):
            try:
                await self.leave_room(room_uuid)
            except ClientError:
                pass

    async def join_room(self, room_uuid):
        """
        Called by receive_json when someone sent a join command.
        """
        room = await get_room_or_error(room_uuid, self.scope['user'])

        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    'type': 'chat.join',
                    'room_uuid': room_uuid,
                    'username': self.scope['user'].username,
                }
            )

        self.rooms.add(room_uuid)

        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )

        await self.send_json({'join': str(room.id)})

    async def leave_room(self, room_uuid):
        """
        Called by receive_json when someone sent a leave command.
        """
        room = await get_room_or_error(room_uuid, self.scope['user'])

        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    'type': 'chat.leave',
                    'room_uuid': room_uuid,
                    'username': self.scope['user'].username,
                }
            )

        self.rooms.discard(room_uuid)

        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )

        await self.send_json({'leave': str(room.id)})

    async def send_room(self, room_uuid, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        if room_uuid not in self.rooms:
            raise ClientError('ROOM_ACCESS_DENIED')

        room = await get_room_or_error(room_uuid, self.scope['user'])
        await self.channel_layer.group_send(
            room.group_name,
            {
                'type': 'chat.message',
                'room_uuid': room_uuid,
                'username': self.scope['user'].username,
                'message': message,
            }
        )

    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        await self.send_json(
            {
                'msg_type': settings.MSG_TYPE_ENTER,
                'room': event['room_uuid'],
                'username': event['username'],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        await self.send_json(
            {
                'msg_type': settings.MSG_TYPE_LEAVE,
                'room': event['room_uuid'],
                'username': event['username'],
            },
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        await self.send_json(
            {
                'msg_type': settings.MSG_TYPE_MESSAGE,
                'room': event['room_uuid'],
                'username': event['username'],
                'message': event['message'],
            },
        )
