# database async connection for real time chat
from channels.db import database_sync_to_async

# from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatMessage
from asgiref.sync import sync_to_async
import json


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user1 = self.scope['user'].username
        user2 = self.room_name
        # Buat nama grup unik untuk 2 user (urutan alfabet)
        self.room_group_name = f"chat_{''.join(sorted([user1, user2]))}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']
        receiver = await self.get_receiver_user()

        await self.save_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.username,
                'receiver': receiver.username,
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message):
        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
        print(f"Pesan berhasil disimpan: {sender} -> {receiver}: {message}")

    @sync_to_async
    def get_receiver_user(self):
        return User.objects.get(username=self.room_name)

# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print('connected', event)
#         user = self.scope['user']
#         chat_room = f'user_chatroom_{user.id}'
#         self.chat_room = chat_room

        
#         await self.channel_layer.group_add(
#             chat_room,
#             self.channel_name
#         )
#         await self.send({
#             'type': 'websocket.accept'
#         })

#     async def websocket_receive(self, event):
#         # data sent by fe, connected to chatroom 
#         received_data = json.loads(event['text'])

#         msg = received_data.get('message')
#         sent_by_id = received_data.get('sent_by')
#         send_to_id = received_data.get('send_to')

#         print(f"RECEIVE WEBSOCKET - Sent by ID: {sent_by_id}, Send to ID: {send_to_id}")  # Debugging log
#         if not msg:
#             print('Error:: empty message')
#             return False
        
        
#         sent_by_user = await self.get_user_object(sent_by_id)
#         send_to_user = await self.get_user_object(send_to_id)
#         if not sent_by_user:
#             print("Error :: sent by user is incorrect")
#             print(f"User with ID {sent_by_id} does not exist.")
#         if not send_to_user:
#             print("Error:: send to user is incorrect")

#         print(f"Received data: {received_data}")
#         print(f"Sent by ID: {sent_by_id}, Send to ID: {send_to_id}")

#         other_user_chat_room = f"User_chatroom_{send_to_id}"
#         self_user = self.scope['user']

#         thread_id = self.scope['url_route']['kwargs'].get('thread_id')
        
#         if not thread_id:
#             print("Error: thread_id not found in URL route")
#         response ={
#             'message': msg,
#             'sent_by': self_user.id,
#             'thread_id': thread_id,
#         }

#         await self.channel_layer.group_send(
#             other_user_chat_room,
#             {
#                 'type' : 'chat_message',
#                 'text' : json.dumps(response),
#             }
#         )

#         await self.channel_layer.group_send(
#             self.chat_room,
#             {
#                 'type' : 'chat_message',
#                 'text' : json.dumps(response),
#             }
#         )

#         # await self.send({
            
#         #     'type': 'websocket.send',
#         #     'text': json.dumps(response)
#         # })
        

#     async def websocket_disconnect(self, event):
#         print('disconnected', event)

#     async def chat_message(self, event):
#         print('chat_message', event)
#         await self.send({
#             'type': 'websocket.send',
#             'text': event['text']
#         })
    
#     @database_sync_to_async
#     def get_user_object(self, user_id):
#         qs = User.objects.filter(id=user_id)
#         if qs.exists():
#             obj = qs.first()
#         else:
#             obj = None
#         return obj


        



# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print('WebSocket connected')
#         await self.accept()

#     async def disconnect(self, close_code):
#         print('WebSocket disconnected')

#     async def receive(self, text_data):
#         print('Message received:', text_data)
#         await self.send(text_data=json.dumps({
#             'message': 'Message received'
#         }))