from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Post title', max_length=100, null=False, blank=False)
    body = models.TextField('Post body', null=False, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def get_absolute_url(self):
        return f'/forum/{self.id}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'
