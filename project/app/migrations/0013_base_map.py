# Generated by Django 4.1.3 on 2022-12-17 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_base_user_seat_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='base',
            name='map',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
