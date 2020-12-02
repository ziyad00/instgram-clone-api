from django.urls import path
from .views import *

app_name = 'images'

urlpatterns = [
   # path('create/', views.image_create, name='create'),
    #path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
   # path('like/', views.image_like, name='like'),
   # path('', views.image_list, name='list'),
    #path('ranking/', views.image_ranking, name='ranking'),
    
    path("images/",ImageListCreateView.as_view(),name="image-list"),
    path("image/<int:pk>",ImageDetailView.as_view(),name="image"),

]
