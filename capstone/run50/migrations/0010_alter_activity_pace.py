# Generated by Django 4.0 on 2021-12-18 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run50', '0009_remove_activity_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='pace',
            field=models.FloatField(null=True),
        ),
    ]
