from django.urls import path
from .consumers import *

# consumers is the equivelant to views in django but for the websocket requests

websocket_urlpatterns = [
    # ws/socket-server/ route is defined in the front end as the endpoint it will reach for 
    path("ws/socket-server/<chatroom_name>",varChatroomConsumer.as_asgi()),
    path("ws/socket-server/",ChatroomConsumer.as_asgi()),
    
]