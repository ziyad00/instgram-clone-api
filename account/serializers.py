from .models import Profile
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        #fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
        


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url',"id", "username", "email"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    real_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.show_real_name = kwargs.pop("show_real_name", False)
        super(UserProfileSerializer, self).__init__(*args, **kwargs)

    def get_real_name(self, obj):
        return obj.real_name if self.show_real_name else None



class EditUserProfileSerializer(serializers.Serializer):
    real_name = serializers.CharField(max_length=32, allow_null=True, required=False)
    photo = serializers.CharField(max_length=256, allow_blank=True, required=False)

