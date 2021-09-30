import json

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer# The class we're using
from asgiref.sync import sync_to_async # Implement later

from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

         # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': message,
            'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
    }))

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)





class MessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        print('room_id', self.room_id)
        print('user_id', self.user_id)
        await self.accept()

        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )

        message_data = await self.get_message_data(self.room_id, self.user_id)
        await self.send_json(message_data)


    async def disconnect(self, event):
        print("disconnected", event)



    # Receive message from WebSocket
    async def receive_json(self, content):
        print("CONTENT", content)
        if content['command'] == "send":
            message = content['message']

            print('message', message)
            
            self.room_name = "room" + str(self.room_id)
            message_data = await self.send_message_data(self.room_id, self.user_id, message)

            # if message_data['result'] == 'false':
                # await self.send_json(message_data)
            # else:
                # message_data = await self.get_message_data(self.room_id, self.user_id)
                # await self.send_json(message_data)

            await self.send_json(message_data)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'recieve_group_message',
                    'message': message
                }
            )



    @sync_to_async
    def send_message_data(self, room_id, user_id, message):
        try:
            Room_obj = Room.objects.get(id=room_id,is_delete=0)
        except:
            result = {'result': 'false', 'Message': 'room id does not match', 'internalCode': '001'}
            return result
        try:
            User_obj = Chat_User.objects.get(id=user_id,is_delete=0)
        except:
            result = {'result': 'false', 'Message': 'user id does not match', 'internalCode': '002'}
            return result

        Participants_obj = Participants.objects.get(room=Room_obj)
        users = Participants_obj.users.all()
        if User_obj in users:
            Messages_obj = Messages.objects.create(room=Room_obj,user=User_obj,message=message)
            Messages_obj_dic = {}
            Messages_obj_dic['message_id'] = Messages_obj.id
            Messages_obj_dic['room_name'] = Messages_obj.room.room_name
            Messages_obj_dic['username'] = Messages_obj.user.username
            Messages_obj_dic['message'] = ''
            Messages_obj_dic['file'] = ''
            if Messages_obj.file:
                Messages_obj_dic['file'] = Messages_obj.file.url
            if Messages_obj.message:
                Messages_obj_dic['message'] = Messages_obj.message
            result = {'result': 'true', 'Message': Messages_obj_dic, 'internalCode': '003'}
        else:
            result = {'result': 'false', 'Message': 'user id does not in group', 'internalCode': '005'}
        return result



    @sync_to_async
    def get_message_data(self, room_id,user_id):
        try:
            Room_obj = Room.objects.get(id=room_id,is_delete=0)
        except:
            result = {'result': 'false', 'Message': 'room id does not match', 'internalCode': '004'}
            return result
        
        try:
            User_obj = Chat_User.objects.get(id=user_id,is_delete=0)
        except:
            result = {'result': 'false', 'Message': 'user id does not match', 'internalCode': '005'}
            return result

        Participants_obj = Participants.objects.get(room=Room_obj)
        users = Participants_obj.users.all()
        if User_obj in users:

            Messages_obj = Messages.objects.filter(room=Room_obj,is_delete=0)
            Messages_obj_list = []
            for i in Messages_obj:
                Messages_obj_dic = {}
                Messages_obj_dic['message_id'] = i.id
                Messages_obj_dic['room_name'] = i.room.room_name
                Messages_obj_dic['username'] = i.user.username
                Messages_obj_dic['message'] = ''
                Messages_obj_dic['file'] = ''
                if i.file:
                    Messages_obj_dic['file'] = i.file.url
                if i.message:
                    Messages_obj_dic['message'] = i.message
                Messages_obj_list.append(Messages_obj_dic)

            result = {'result': 'true', 'Message': Messages_obj_list, 'internalCode': '005'}
        else:
            result = {'result': 'false', 'Message': 'user id does not in group', 'internalCode': '005'}

        return result