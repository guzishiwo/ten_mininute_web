# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 02:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_remove_video_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_collected', models.BooleanField(default=False)),
                ('users', models.ManyToManyField(related_name='video', to='website.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='is_collect',
        ),
        migrations.AddField(
            model_name='collection',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='website.Video'),
        ),
    ]
