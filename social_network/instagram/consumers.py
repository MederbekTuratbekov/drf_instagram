import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        await self.save_message(user, self.room_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "author": user.username}
        )

    async def chat_message(self, event):
        message = event["message"]
        author = event.get("author")
        await self.send(text_data=json.dumps({"message": message, "author": author}))

    @database_sync_to_async
    def save_message(self, user, room_name, message):
        chat, _ = Chat.objects.get_or_create(id=room_name)
        Message.objects.create(author=user, text=message, chat=chat)
