from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import FollowView, ProfileListCreateView,ProfileDetailView

from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt

app_name = 'account'
urlpatterns = [

    #path('', api_root),

    path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'})),
    path("profiles/",ProfileListCreateView.as_view(),name="all-profiles"),
    path("profile/<int:pk>",ProfileDetailView.as_view(),name="profile"),

]
