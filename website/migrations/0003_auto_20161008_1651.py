# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-08 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20161008_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='belong_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='under_comments', to='website.Article'),
        ),
    ]
