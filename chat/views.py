from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import utils
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

# it automaticaly redirect the user if not loged in to the page specified in the settimgs LOGIN_URL = ''
@login_required
def main_chat_view(request,group_name=None):
    if group_name:
        return render(request ,'chat/base.html',{'groupname':group_name})  
    else:
        #in the model iam setting the __str_- to return the name not the id 
        group_name= get_object_or_404(Chat_group, group_name="Main")
        group_messages_list= Messages.objects.filter(group=group_name)
        print(request.user)
        
        context ={
            'messages_list': group_messages_list,
            'View_request_user':request.user
        }
        
        return render(request ,'chat/base.html', context)

    
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if utils.checkpassword(password) and utils.is_uniqe(username):
            newuser = User.objects.create(
                username=username,
                password=make_password(password)
            )
            newuser.save()
            return redirect('login')    
        else:
            return redirect('signup')    
            
    else:
        return render(request ,'chat/signup.html')    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        if utils.login_val(username ,password):
            # el function dy bt3ml nfs ely login_val bt3mlo blzabt bs m4 2ader azabat el code
            user = authenticate(request, username=username, password=password)
            #loging the user in django system (by storing the user details in the session) so he dont become an anonymous user 
            auth_login(request, user)
            return redirect('home')
        else :
            return redirect('login')
    else: 
        return render(request ,'chat/login.html')
