# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-08 08:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='belong_to',
            field=models.ForeignKey(blank=True, null=None, on_delete=django.db.models.deletion.CASCADE, related_name='under_comments', to='blog.Article'),
        ),
    ]
