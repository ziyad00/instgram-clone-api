from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)

    def __str__(self):
        return str(self.id)
    
    



class Comment(models.Model):
    image = models.ForeignKey(Image,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments_created',
                             on_delete=models.CASCADE)

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body