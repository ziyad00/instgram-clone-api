from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.permissions import AllowAny,IsAuthenticated
#from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
from .models import Profile
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import ProfileSerializer, ActionSerializer
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
import os
from datetime import timedelta
from importlib import import_module
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from otpauth import OtpAuth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.http import JsonResponse

from rest_framework import mixins
from rest_framework import generics





class FollowView(viewsets.ViewSet):
    queryset = Profile.objects.all()

    def follow(self, request, pk):
        #own_profile = request.user.profile.first() # or your queryset to get
        following_profile = Profile.objects.get(id=pk)
        request.user.profile.following.add(get_user_model().objects.get(id=pk))  # and .remove() for unfollow
        return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)
    def unfollow(self, request, pk):
       # own_profile = request.user.profile_set.first()  # or your queryset to get
        #following_profile = Profile.objects.get(id=pk)
        request.user.profile.following.remove(get_user_model().objects.get(id=pk))  # and .remove() for unfollow
        return Response({'message': 'now you are not following'}, status=status.HTTP_200_OK)



class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    
 
    def perform_create(self, serializer):
        user=self.request.user
        serializer =serializer.save(user=user)

        
    def get_permissions(self):        
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
   
    
class ActionDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def get(self, request, *args, **kwargs):
        
        actions = Action.objects.exclude(user=request.user)

        following_ids = request.user.profile.following.values_list('id',
                                                       flat=True)
        if following_ids:
                # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
                        .prefetch_related('target')[:10]
        x = ActionSerializer(actions, many=True)
        print(x)
        return Response(x.data, status=status.HTTP_200_OK)

    

   
class followersView(APIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get(self, request, *args, **kwargs):
        
           # get image ranking dictionary
        image_ranking = r.zrange('image_ranking', 0, -1, desc=True)
        image_ranking_ids = [int(id) for id in image_ranking]
        # get most viewed images
        most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
        x = ImageSerializer(most_viewed, many=True)
        return Response(x.data, status=status.HTTP_200_OK)
