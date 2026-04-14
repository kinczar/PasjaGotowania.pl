from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField #strona do zdjęc w bazie danych

class Post(models.Model):

    POST_TYPES = [
        ('recipe', 'Przepis'),
        ('question', 'Porada'),
    ]

    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES,
        default='recipe'
    )
        
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Post title', max_length=100, null=False, blank=False)
    calories = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=100, null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
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

    parent = models.ForeignKey( #odpowiadanie na komentarze
        'self', 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)

    def total_likes(self):
        return self.likes.count()

    def is_reply(self):
        return self.parent is not None

