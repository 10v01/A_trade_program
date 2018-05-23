# Generated by Django 2.0.5 on 2018-05-12 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0010_auto_20180512_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentBindingMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='currentbindingmail',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.Profile'),
        ),
    ]