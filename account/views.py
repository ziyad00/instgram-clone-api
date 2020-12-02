from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.permissions import AllowAny,IsAuthenticated
#from common.decorators import ajax_required
#from actions.utils import create_action
#from actions.models import Action
from .models import Profile
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import ProfileSerializer
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






#@api_view(['GET'])
#def api_root(request):
 #   return Response({
  #      'users': reverse('user-list', request=request),
   #     'user_register_api': reverse('user_register_api', request=request)
   # })
    

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
    def get_queryset(self):
        user = self.request.user
        return user.purchase_set.all()
    
class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsOwnerOrReadOnly,IsAuthenticated]