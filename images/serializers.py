from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer




class CommentSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True, source='user.id')
    #user = UserSerializer()  # May be an anonymous user.
    #user = serializers.Field(source='user.username')

    class Meta:
        model=Comment
        fields='__all__'
        #exclude = ('user',)



class ImageSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True, source='user.id')
    #comments = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model=Image
        fields='__all__'
        #fields= ('id','user','image','description','created')
        #exclude = ('users_like', 'total_likes')
        read_only_fields = ('users_like', 'total_likes')

 