from django.db import models

class Post(models.Model):
    title = models.CharField('Post title', max_length=100, null=False, blank=False)
    body = models.TextField('Post body', null=False, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'
