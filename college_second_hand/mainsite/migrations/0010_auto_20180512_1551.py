# Generated by Django 2.0.5 on 2018-05-12 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_auto_20180512_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='male',
            new_name='sex',
        ),
    ]
