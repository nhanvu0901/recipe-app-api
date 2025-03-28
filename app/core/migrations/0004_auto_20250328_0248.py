# Generated by Django 3.2.25 on 2025-03-28 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customtoken',
            name='key',
        ),
        migrations.AddField(
            model_name='customtoken',
            name='access_token',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customtoken',
            name='refresh_token',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]
