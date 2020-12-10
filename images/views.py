from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
                                  PageNotAnInteger
from actions.utils import create_action
from rest_framework import generics

from .models import *
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from account.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView

import redis
from django.conf import settings

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                 db=settings.REDIS_DB)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    def retrieve(self, request, pk=None):
        queryset = Image.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image)
        total_views = r.incr(f'image:{image.id}:views')
        r.zincrby('image_ranking', 1, image.id)
        return Response(serializer.data)
        
    def perform_create(self, serializer):
        user=self.request.user
        serializer =serializer.save(user=user)
        create_action(self.request.user, 'post image', serializer)

    
    #def retrieve(self, request, pk=None):
     #   image = self.get_object()
      #  total_views = r.incr(f'image:{image.id}:views')

        
    def get_permissions(self):        
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Image.objects.all()
        if self.action == 'list':
            username = self.request.query_params.get('username', None)
            if username is not None:
                userID = User.objects.get(username=username)
                queryset = queryset.filter(user=userID)
        elif self.action == 'detail':
            total_views = r.incr(f'image:{image.id}:views')
            r.zincrby('image_ranking', 1, image.id)


        return queryset

    


class LikeView(viewsets.ViewSet):
    queryset = Image.objects.all()

    def like(self, request, pk):
        image = Image.objects.get(id=pk)
        image.users_like.add(request.user)
        return Response({'message': 'now you like the image'}, status=status.HTTP_200_OK)
        
    
    def dislike(self, request, pk):
        image = Image.objects.get(id=pk)
        image.users_like.remove(request.user)
        return Response({'message': 'now you don\t like the image'}, status=status.HTTP_200_OK)

   
    def get_queryset(self):
        user = self.request.user
        return user.purchase_set.all()
    
 

    
class ExplorerView(APIView):
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    
 
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
    
   