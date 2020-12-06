from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
   # path('create/', views.image_create, name='create'),
    #path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
   # path('like/', views.image_like, name='like'),
   # path('', views.image_list, name='list'),
    #path('ranking/', views.image_ranking, name='ranking'),
   path('', include(router.urls)),
   path('like/<int:pk>/', LikeView.as_view({'post': 'like'})),

 #   path("images/",ImageListCreateView.as_view(),name="image-list"),
  #  path("image/<int:pk>",ImageDetailView.as_view(),name="image"),

]
