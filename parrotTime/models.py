from django.db import models

class Parrot(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    gif_url = models.TextField()

    def __str__(self):
        return self.name
