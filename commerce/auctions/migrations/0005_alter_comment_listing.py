# Generated by Django 3.2.8 on 2021-10-14 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ManyToManyField(default=None, related_name='comments', to='auctions.Listing'),
        ),
    ]
