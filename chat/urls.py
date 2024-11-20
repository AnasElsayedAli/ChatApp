from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #main chatgroup 
    path('chat/',views.main_chat_view,name="home"),
    path('chat/<group_name>',views.main_chat_view),
    path('',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    
    
    
]
