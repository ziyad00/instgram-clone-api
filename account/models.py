from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser



#class User(AbstractUser):
#     email = models.EmailField(verbose_name='email', max_length=255, unique=True)
#     phone = models.CharField(null=True, max_length=255)
#     REQUIRED_FIELDS = ['username','first_name', 'password']
#     USERNAME_FIELD = 'email'


 #    def __str__(self):
  #        return f'Profile for user {self.user.username}'

UserModel = get_user_model()
  
class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE,  related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    real_name = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=255)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)


    def __str__(self):
        return f'Profile for user {self.user.username}'

