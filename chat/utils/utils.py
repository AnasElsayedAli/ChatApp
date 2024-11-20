from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

def checkpassword(password):
    if len(password) < 8:
        return False
    else:
        return True
        
def is_uniqe(username):
    database_user = User.objects.filter(username=username).first()
    if database_user :
        return False 
    else:
        return True
    
def login_val(usernam,password):
    user = User.objects.filter(username=usernam).first()
    if user :
        database_user_password = user.password
        if check_password(password, database_user_password):
            return True
        else :
            return False
    else:
        return False    