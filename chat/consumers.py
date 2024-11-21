from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404 ,render
from .models import *
from django.template.loader import render_to_string


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        #adding member to group.members
        self.user=self.scope['user']
        is_user_member = Chat_group.objects.filter(group_name='Main').filter( members=self.user)
        if is_user_member:
            pass
        else:
            Main=Chat_group.objects.get(group_name='Main')
            Main.members.add(self.user)
        # End  adding member to group.members  
        
        
        # adding channel to group
        self.group = get_object_or_404(Chat_group,group_name='Main') 
        async_to_sync(self.channel_layer.group_add)(
            self.group.group_name,
            self.channel_name
        )
        self.accept()
        #End adding channel to group
        
        
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group.group_name,
            self.channel_name
        )   
    
    
    def receive(self,text_data): 
        parsed_text_data = json.loads(text_data)
        #iam sending it from the front end as message --> chatsocket.send(JSON.stringify({'message':message})
        message = parsed_text_data['message']
        print(self.user)
        Message =Messages.objects.create(
            body=message,
            author =self.user,
            group =self.group
        )
        Message.save()
        
        event = {
                #the type here refer to the function that will actualy send the message 
                'type':'chat_messages',
                'message': Message,
            }
        
        async_to_sync(self.channel_layer.group_send)(
            self.group.group_name,
            #in the event i send the function name and the message 
            #this whole event obj will be sent to the chat_messages function so i can access both type , message 
            event
        )
    def chat_messages(self,event):
        message = event['message']
        message_body=message.body
        message_author=message.author.username
        text_data = json.dumps({
        'type':'text',
        'message_body':message_body,  
        'message_author':message_author        
        })  
        self.send(text_data) 
        
class varChatroomConsumer(WebsocketConsumer):  
    def connect(self):
        self.user=self.scope['user']
        #i extract the chat_room name part from the url that is sent to router--> "ws/socket-server/<chatroom_name>"
        self.group_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.group = get_object_or_404(Chat_group,group_name=self.group_name) 
        async_to_sync(self.channel_layer.group_add)(
            self.group.group_name,
            self.channel_name
        )
        self.accept() 
            
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
        self.group.group_name,
        self.channel_name
    )        
    
    def receive(self,text_data): 
        parsed_text_data = json.loads(text_data)
        #iam sending it from the front end as message --> chatsocket.send(JSON.stringify({'message':message})
        message = parsed_text_data['message']
        Message =Messages.objects.create(
            body=message,
            author =self.user,
            group =self.group
        )
        Message.save()
        
        event = {
                #the type here refer to the function that will actualy send the message 
                'type':'chat_messages',
                'message': Message,
            }
        
        async_to_sync(self.channel_layer.group_send)(
            self.group.group_name,
            #in the event i send the function name and the message 
            #this whole event obj will be sent to the chat_messages function so i can access both type , message 
            event
        )
    def chat_messages(self,event):
        message = event['message']
        message_body=message.body
        message_author=message.author.username
        text_data = json.dumps({
        'type':'text',
        'message_body':message_body,  
        'message_author':message_author        
        })  
        self.send(text_data) 
            