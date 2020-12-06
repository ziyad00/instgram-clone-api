from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
                                  PageNotAnInteger
#from common.decorators import ajax_required
#from actions.utils import create_action

#from .forms import ImageCreateForm
from .models import *
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from account.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser

from rest_framework import viewsets

import redis
from django.conf import settings

# connect to redis
#r = redis.Redis(host=settings.REDIS_HOST,
  #              port=settings.REDIS_PORT,
   #             db=settings.REDIS_DB)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    
    #def create(self, request):
      #  user=self.request.user
       # serializer_class.save(user=user)
        
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)    
        
    def get_permissions(self):        
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
  #  def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        #user = self.request.user
        #return Image.objects.filter(user=user)
    
#class ImageListCreateView(ListCreateAPIView):
    #queryset = Image.objects.all()
    #serializer_class= ImageSerializer
    #permission_classes=[IsAuthenticated]

    #def perform_create(self, serializer):
     #   user=self.request.user
    #    serializer.save(user=user)


#class ImageDetailView(RetrieveUpdateDestroyAPIView):
 #   queryset=Image.objects.all()
  #  serializer_class=ImageSerializer
   # permission_classes=[IsOwnerOrReadOnly,IsAuthenticated]






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