# Generated by Django 3.2.8 on 2021-11-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_rename_follower_follower_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
