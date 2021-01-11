from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


#class User(AbstractUser):
#     email = models.EmailField(verbose_name='email', max_length=255, unique=True)
#     phone = models.CharField(null=True, max_length=255)
#     REQUIRED_FIELDS = ['username','first_name', 'password']
#     USERNAME_FIELD = 'email'


 #    def __str__(self):
  #        return f'Profile for user {self.user.username}'

  
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    #photo = CloudinaryField('avatar')
    real_name = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=255)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)


    def __str__(self):
        return f'Profile for user {self.user.username}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)