# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_auto_20161016_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
