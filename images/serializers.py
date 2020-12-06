from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model





class ImageSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Image
        fields= ('id','user','image','description','created')
        #exclude = ('users_like', 'total_likes')
    
 