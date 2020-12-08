from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer





class ImageSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
   # UserSerializer()
    
    class Meta:
        model=Image
        fields= ('id','user','image','description','created')
        #exclude = ('users_like', 'total_likes')
    
 