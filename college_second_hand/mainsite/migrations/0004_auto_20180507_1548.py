# Generated by Django 2.0.5 on 2018-05-07 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_auto_20180507_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='profile',
            new_name='buyer',
        ),
    ]