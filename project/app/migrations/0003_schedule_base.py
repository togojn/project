# Generated by Django 4.1.3 on 2022-11-10 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_schedule_seat'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='base',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.base', verbose_name='拠点'),
            preserve_default=False,
        ),
    ]