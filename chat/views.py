from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

# return my template to show the users the chat messages
def main_chat_view(request,group_name=None):
    if group_name:
        return render(request ,'chat/base.html',{'groupname':group_name})  
    else:
        #in the model iam setting the __str_- to return the name not the id 
        group_name= get_object_or_404(Chat_group, group_name="Main")
        group_messages_list= Messages.objects.filter(group=group_name)
        
        
        context ={
            'messages_list': group_messages_list,
            'View_request_user':request.user
        }
        
        return render(request ,'chat/base.html', context)

