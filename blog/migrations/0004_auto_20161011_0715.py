# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20161008_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(null=True, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='create_on',
            field=models.DateField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='hits',
            field=models.IntegerField(verbose_name=b'\xe7\x82\xb9\xe5\x87\xbb\xe9\x87\x8f'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=128, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='update_on',
            field=models.DateField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=500, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=50, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0', blank=True),
        ),
    ]
