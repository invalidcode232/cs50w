# Generated by Django 3.2.8 on 2021-11-13 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20211113_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='follower',
            new_name='following',
        ),
    ]