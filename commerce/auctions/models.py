from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="author_listings")
    name = models.CharField(max_length=64)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    image_url = models.URLField(max_length=200)
    bids = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist_users = models.ManyToManyField(User, related_name="watchlist_listings", null=True, blank=True)
    is_open = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, related_name="category_listings", default=None)

    def __str__(self):
        return f"{self.name} by {self.user} | {self.created_at}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing = models.ManyToManyField(Listing, default=None, related_name="comments")
    content = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment at {self.listing} by {self.user} | {self.created_at}"
