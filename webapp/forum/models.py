from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField #strona do zdjęc w bazie danych

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Post title', max_length=100, null=False, blank=False)
    body = models.TextField('Post body', null=False, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image', blank=True, null=True, folder='posts/') #nazwa specjalnego pola dla aplikacji do trzymanai zdjęć w bazie

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)


#model komentarza
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)