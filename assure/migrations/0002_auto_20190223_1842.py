# Generated by Django 2.1.5 on 2019-02-24 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assure', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pilot',
            name='viewport_duration',
        ),
        migrations.RemoveField(
            model_name='pilot',
            name='viewport_json',
        ),
        migrations.RemoveField(
            model_name='pilot',
            name='viewport_result',
        ),
    ]