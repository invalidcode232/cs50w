# Generated by Django 3.2.8 on 2021-10-16 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20211015_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
