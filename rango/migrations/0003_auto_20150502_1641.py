# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20150428_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='category',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firstName',
            field=models.CharField(default='null', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastName',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
