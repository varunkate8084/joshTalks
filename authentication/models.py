from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
  login_method = models.CharField(max_length=20,default='email')
    
