from django.db import models

# Create your models here.

from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    prep_time = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title