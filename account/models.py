from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    real_name = models.TextField(null=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)


    def __str__(self):
        return f'Profile for user {self.user.username}'
