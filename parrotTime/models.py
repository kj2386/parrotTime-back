from django.db import models
from django.conf import settings


class Parrot(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    gif_url = models.TextField()

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    parrot = models.ForeignKey(Parrot, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.parrot.name}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parrots = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
