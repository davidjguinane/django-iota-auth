# Generated by Django 2.0 on 2017-12-25 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iota_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
