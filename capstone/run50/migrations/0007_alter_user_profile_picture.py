# Generated by Django 4.0 on 2021-12-17 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run50', '0006_activity_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', upload_to='profile_pictures'),
        ),
    ]
