# Generated by Django 2.0.5 on 2018-05-13 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0019_order_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
