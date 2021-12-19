from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    share_preference = models.IntegerField(default=0)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures', default='profile_pictures/default.jpg')


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    distance = models.IntegerField()
    duration = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to='activity_images', blank=True)
    elevation = models.IntegerField(null=True)
    pace = models.FloatField(null=True)
    heart_rate = models.IntegerField(null=True)
    # location = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Run on {self.date} at {self.time}'


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.follower.username}'
