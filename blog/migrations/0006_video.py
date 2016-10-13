# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-11 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20161011_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('url_image', models.URLField(blank=True, null=True)),
                ('editor_choice', models.BooleanField(default=False)),
            ],
        ),
    ]
