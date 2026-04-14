from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            try:
                return self.profile_picture.url
            except:
                pass
        return static('main/images/default-profile.png')
