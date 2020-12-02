from django.contrib.auth.models import  Group
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model





class ProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    #user = UserSerializer()  # May be an anonymous user.

    class Meta:
        model=Profile
        fields='__all__'