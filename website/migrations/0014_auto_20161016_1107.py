# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20161016_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_collected',
        ),
        migrations.AddField(
            model_name='video',
            name='is_collected',
            field=models.BooleanField(default=False),
        ),
    ]
