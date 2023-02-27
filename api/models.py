from django.db import models

# Create your models here.
class Character(models.Model):
    fr_name = models.CharField(max_length=100, null=True)
    fr_description = models.TextField(null=True)
    image = models.URLField()
    fr_general_infos = models.JSONField(null=True)
    en_name = models.CharField(max_length=100, null=True)
    en_description = models.TextField(null=True)
    en_general_infos = models.JSONField(null=True)

    def __str__(self):
        if self.en_name is None:
            return self.fr_name
        else:
            return self.en_name

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100)
    characters = models.ManyToManyField(Character, related_name='fr_categories')
    def __str__(self):
        return self.en_name