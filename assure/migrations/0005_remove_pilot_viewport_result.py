# Generated by Django 2.1.5 on 2019-02-25 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assure', '0004_pilot_viewport_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pilot',
            name='viewport_result',
        ),
    ]
