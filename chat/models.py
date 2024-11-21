from django.db import models
from django.contrib.auth.models import User
# short uuid create short and unique id 
import shortuuid
# Create your models here.

class Chat_group(models.Model):
    group_name = models.CharField(max_length=150,unique=True,default =shortuuid.uuid)
    # the related name will be used when iam on the other model and trying to access this model
    members = models.ManyToManyField(User,related_name="chat_groups",blank=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.group_name

class Messages(models.Model):
    group = models.ForeignKey(Chat_group,related_name ='chat_message',on_delete=models.CASCADE)    
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length = 300)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author} : {self.body}"

