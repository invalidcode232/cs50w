from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=64)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    image_url = models.URLField(max_length=200)
    bids = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user} | {self.created_at}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing = models.ManyToManyField(Listing, default=None, related_name="comments")
    content = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
