# Generated by Django 2.0.5 on 2018-05-12 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0016_auto_20180512_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='update_at',
        ),
    ]
