from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from forum.models import Post
from main.models import Recipe


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Post)
def create_recipe_from_post(sender, instance, created, **kwargs):
    if instance.post_type == 'recipe':
        Recipe.objects.update_or_create(
            title=instance.title,
            author=instance.author,
            defaults={
                'calories': instance.calories,
                'servings': instance.servings,
            }
        )