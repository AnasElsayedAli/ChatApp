from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #main chatgroup 
    path('',views.main_chat_view),
    path('<group_name>',views.main_chat_view),
    
]
