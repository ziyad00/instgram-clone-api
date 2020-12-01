from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.permissions import AllowAny
#from common.decorators import ajax_required
#from actions.utils import create_action
#from actions.models import Action
from .models import Profile
from .permissions import IsOwnerProfileOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer,ProfileSerializer
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
#from .serializers import (UserProfileSerializer, EditUserProfileSerializer)
#from .tasks import send_email_async



#class UserProfileAPI(APIView):
    #@method_decorator(ensure_csrf_cookie)
    #def get(self, request, **kwargs):
      
        #user = request.user
        #if not user.is_authenticated:
         #   return self.success()
        #show_real_name = False
        #username = request.GET.get("username")
        #try:
            #if username:
           #     user = User.objects.get(username=username)
          #  else:
         #       user = request.user
        #        show_real_name = True
       # except User.DoesNotExist:
      #      return self.error("User does not exist")
     #   return self.success(UserProfileSerializer(user.profile, show_real_name=show_real_name).data)

    #@validate_serializer(EditUserProfileSerializer)
   # @login_required
  #  def put(self, request):
 #       data = request.data
 #       user_profile = request.user.Profile
#        for k, v in data.items():
#            setattr(user_profile, k, v)
#        user_profile.save()
#        return self.success(UserProfileSerializer(user_profile, show_real_name=True).data)


#class AvatarUploadAPI(APIView):
  #  request_parsers = ()

   # @login_required
    #def post(self, request):
     #   form = ImageUploadForm(request.POST, request.FILES)
      #  if form.is_valid():
       #     avatar = form.cleaned_data["image"]
        #else:
         #   return self.error("Invalid file content")
       # if avatar.size > 2 * 1024 * 1024:
        #    return self.error("Picture is too large")
       # suffix = os.path.splitext(avatar.name)[-1].lower()
       # if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
        #    return self.error("Unsupported file format")

        #name = rand_str(10) + suffix
        #with open(os.path.join(settings.AVATAR_UPLOAD_DIR, name), "wb") as img:
         #   for chunk in avatar:
          #      img.write(chunk)
        #user_profile = request.user.userprofile

        #user_profile.avatar = f"{settings.AVATAR_URI_PREFIX}/{name}"
        #user_profile.save()
        #return self.success("Succeeded")







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
    queryset=uProfile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]