# Generated by Django 2.2.5 on 2019-09-12 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_userprofile_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_joined',
        ),
    ]
