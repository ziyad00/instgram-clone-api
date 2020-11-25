from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
                        FollowView,
                        UserList,UserDetail,
                          api_root)

from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    #path('', api_root),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

   # path("profile/", UserProfileAPI.as_view(), name="user_profile_api"),
    #path("upload_avatar/", AvatarUploadAPI.as_view(), name="avatar_upload_api"),

    path('users/', UserList.as_view(), name="user-list"),
    path('users/<int:pk>/', UserDetail.as_view(), name="user-detail"),
    path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'})),


]
