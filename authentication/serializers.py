from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','last_login','is_superuser','is_staff','groups','user_permissions','first_name','last_name']
