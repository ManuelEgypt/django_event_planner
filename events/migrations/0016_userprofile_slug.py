# Generated by Django 2.2.5 on 2019-09-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_orgprofile_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
