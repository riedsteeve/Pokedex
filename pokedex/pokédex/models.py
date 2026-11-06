from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    level = models.IntegerField()
    image_url = models.URLField()

    def __str__(self):
        return self.name