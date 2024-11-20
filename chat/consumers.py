from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404 ,render
from .models import *
from django.template.loader import render_to_string


class ChatroomConsumer(WebsocketConsumer):
    # defines what happen when a user connects to the web socket
    def connect(self):
        # normaly this name will be taken from the url or from the front end
        self.user=self.scope['user']
        self.group = get_object_or_404(Chat_group,group_name='Main')
        # channel_name is created automaticaly for each user 
        async_to_sync(self.channel_layer.group_add)(
            self.group.group_name,
            self.channel_name
        )
        self.accept()
        #json.dumps convert python obj to json string
        
        
    def disconnect(self,close_code):
        #remove the user channel from the group so he wont receive more updates
        async_to_sync(self.channel_layer.group_discard)(
            self.group.group_name,
            self.channel_name
        )   
    
    def receive(self,text_data):
        #parsing the data from json string into python 
        parsed_text_data = json.loads(text_data)
        #iam sending it from the front end as message --> chatsocket.send(JSON.stringify({'message':message})
        message = parsed_text_data['message']
        Message =Messages.objects.create(
            body=message,
            # lazem akon 3amel nzam login
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
        print("printing from dynamic route")
        self.accept()     