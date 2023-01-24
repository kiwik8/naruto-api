from django.db import models

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    general_infos = models.JSONField()
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    characters = models.ManyToManyField(Character, related_name='categories')
    
    def __str__(self):
        return self.name