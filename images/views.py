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
        try:
            image = Image.objects.get(id=pk)
            image.users_like.add(request.user)
            Response({'message': 'now you like the image'}, status=status.HTTP_200_OK)
        except:
            pass
    
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
        image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        # get most viewed images
        most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
        x = ImageSerializer(most_viewed, many=True)
        return Response(x.data, status=status.HTTP_200_OK)

    
'''


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image,
                   'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 1)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed})

'''