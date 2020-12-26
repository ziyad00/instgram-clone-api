from django.urls import path, include
from django.contrib.auth import views as auth_views


from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'account'

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [

   path('', include(router.urls)),

    path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'})),
    path('timeline/', ActionDetail.as_view()),

  

]
