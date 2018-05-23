# Generated by Django 2.0.5 on 2018-05-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0021_auto_20180514_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_binding_key',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='pay_binding_key',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='state',
            field=models.IntegerField(default=-1),
        ),
    ]